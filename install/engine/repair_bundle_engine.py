import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, Optional

ROOT = Path(__file__).resolve().parents[2]

FAILED_DIR = ROOT / "failed_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"
BRAIN_REPORTS = ROOT / "brain_reports"

REPAIR_WORKER = ROOT / "install" / "engine" / "repair_bundle.py"
REPORT_PATH = BRAIN_REPORTS / "repair_bundle_engine_result.json"

REPAIRED_DIR.mkdir(parents=True, exist_ok=True)
BRAIN_REPORTS.mkdir(parents=True, exist_ok=True)


def now_ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def load_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def resolve_bundle_path(target: str) -> str:
    """
    Resolve bundle location across possible directories.

    Resolution order:
      1. exact path as provided
      2. failed_bundles/<target>
      3. incoming_bundles/<target>
      4. repaired_bundles/<target>
    """
    if not target:
        return ""

    candidate = Path(target)
    if candidate.exists():
        return str(candidate.resolve())

    failed_path = FAILED_DIR / target
    if failed_path.exists():
        return str(failed_path.resolve())

    incoming_path = INCOMING_DIR / target
    if incoming_path.exists():
        return str(incoming_path.resolve())

    repaired_path = REPAIRED_DIR / target
    if repaired_path.exists():
        return str(repaired_path.resolve())

    return ""


def run_worker(bundle_path: str) -> Dict[str, Any]:
    """
    Execute the deterministic repair worker and capture its structured output.
    """
    start = time.time()

    try:
        result = subprocess.run(
            ["python", str(REPAIR_WORKER), "--target", bundle_path],
            capture_output=True,
            text=True,
            cwd=str(ROOT)
        )
    except Exception as e:
        return {
            "ok": False,
            "returncode": 1,
            "stdout": "",
            "stderr": str(e),
            "duration": 0.0,
            "parsed_stdout": None,
            "worker_report": None
        }

    duration = round(time.time() - start, 3)

    parsed_stdout = None
    stdout = result.stdout.strip()

    if stdout:
        try:
            parsed_stdout = json.loads(stdout)
        except Exception:
            parsed_stdout = None

    worker_report = load_json(ROOT / "brain_reports" / "repair_bundle_result.json")

    return {
        "ok": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": stdout,
        "stderr": result.stderr.strip(),
        "duration": duration,
        "parsed_stdout": parsed_stdout,
        "worker_report": worker_report
    }


def propose_repair(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    ts = now_ts()

    target = action_payload.get("target")
    family = action_payload.get("family", "unknown")
    action = action_payload.get("action", "unknown")

    result: Dict[str, Any] = {
        "status": "failed",
        "ts": ts,
        "action": action,
        "family": family,
        "target": target,
        "resolved_path": None,
        "worker_result": None,
        "reason": None,
        "output_report": str(REPORT_PATH)
    }

    if not target:
        result["reason"] = "missing_target"
        write_json(REPORT_PATH, result)
        return result

    resolved_path = resolve_bundle_path(target)
    result["resolved_path"] = resolved_path

    if not resolved_path:
        result["reason"] = "bundle_not_found"
        write_json(REPORT_PATH, result)
        return result

    if not REPAIR_WORKER.exists():
        result["reason"] = "repair_worker_missing"
        write_json(REPORT_PATH, result)
        return result

    worker_result = run_worker(resolved_path)
    result["worker_result"] = worker_result

    worker_report = worker_result.get("worker_report") or {}
    worker_status = worker_report.get("status")

    if worker_result.get("ok") and worker_status == "repaired":
        result["status"] = "ok"
        result["reason"] = "repair_completed"
        result["original_bundle"] = resolved_path
        result["repaired_bundle"] = worker_report.get("output_bundle")
        result["changes_applied"] = worker_report.get("changes_applied", [])
        result["hash_before"] = worker_report.get("hash_before")
        result["hash_after"] = worker_report.get("hash_after")
    else:
        result["status"] = "failed"
        result["reason"] = "repair_worker_failed"
        result["original_bundle"] = resolved_path
        result["repaired_bundle"] = None
        result["changes_applied"] = worker_report.get("changes_applied", [])
        result["hash_before"] = worker_report.get("hash_before")
        result["hash_after"] = worker_report.get("hash_after")

    write_json(REPORT_PATH, result)
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Loop-facing repair bundle engine."
    )
    parser.add_argument(
        "--action-payload-json",
        default="",
        help="Raw JSON string for the action payload."
    )
    parser.add_argument(
        "--target",
        default="",
        help="Direct target bundle path or bundle name."
    )
    parser.add_argument(
        "--family",
        default="unknown",
        help="Optional family name when using direct args."
    )
    args = parser.parse_args()

    action_payload: Dict[str, Any]

    if args.action_payload_json:
        try:
            action_payload = json.loads(args.action_payload_json)
        except Exception:
            action_payload = {
                "action": "propose_repair_for_bundle_family",
                "target": args.target,
                "family": args.family
            }
    else:
        action_payload = {
            "action": "propose_repair_for_bundle_family",
            "target": args.target,
            "family": args.family
        }

    result = propose_repair(action_payload)

    print(json.dumps({
        "status": result["status"],
        "output": str(REPORT_PATH),
        "result": result
    }, indent=2))


if __name__ == "__main__":
    main()

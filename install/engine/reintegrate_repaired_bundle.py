import os
import json
import shutil
import time
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

ROOT = Path(__file__).resolve().parents[2]

FAILED_DIR = ROOT / "failed_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"
BRAIN_REPORTS = ROOT / "brain_reports"

REPORT_PATH = BRAIN_REPORTS / "reintegrate_repaired_bundle_result.json"

INCOMING_DIR.mkdir(parents=True, exist_ok=True)
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
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, str):
            data = json.loads(data)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def resolve_repaired_bundle(path_or_name: str) -> str:
    if not path_or_name:
        return ""

    candidate = Path(path_or_name)
    if candidate.exists():
        return str(candidate.resolve())

    alt = REPAIRED_DIR / path_or_name
    if alt.exists():
        return str(alt.resolve())

    return ""


def run_step(cmd: list[str]) -> Dict[str, Any]:
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True
        )
        return {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
            "duration": round(time.time() - start, 3)
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": round(time.time() - start, 3)
        }


def reintegrate(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    ts = now_ts()

    repaired_bundle = action_payload.get("repaired_bundle") or action_payload.get("target")
    family = action_payload.get("family", "unknown")
    original_bundle = action_payload.get("original_bundle", "")

    result: Dict[str, Any] = {
        "status": "failed",
        "ts": ts,
        "family": family,
        "repaired_bundle": repaired_bundle,
        "resolved_repaired_bundle": None,
        "incoming_bundle": None,
        "original_bundle": original_bundle,
        "original_failed_removed": False,
        "inspection_result": None,
        "reason": None,
        "output_report": str(REPORT_PATH)
    }

    resolved = resolve_repaired_bundle(repaired_bundle)
    result["resolved_repaired_bundle"] = resolved

    if not resolved:
        result["reason"] = "missing_repaired_bundle"
        write_json(REPORT_PATH, result)
        return result

    bundle_name = os.path.basename(resolved)
    incoming_path = INCOMING_DIR / bundle_name

    try:
        shutil.copy2(resolved, incoming_path)
    except Exception as e:
        result["reason"] = "copy_to_incoming_failed"
        result["error"] = str(e)
        write_json(REPORT_PATH, result)
        return result

    result["incoming_bundle"] = str(incoming_path.resolve())

    inspect_payload = {
        "action": "inspect_incoming_bundle_family",
        "action_class": "inspection",
        "target": str(incoming_path.resolve()),
        "family": family,
        "source": "reintegrate_repaired_bundle"
    }

    inspect_step = run_step([
        "python",
        "install/engine/inspect_bundle_engine.py",
        "--action-payload-json",
        json.dumps(inspect_payload)
    ])
    result["inspection_result"] = inspect_step

    inspection_report = load_json(BRAIN_REPORTS / "inspection_result.json") or {}
    inspection = inspection_report.get("inspection", {})
    decision = inspection.get("decision", {})
    action = decision.get("action")

    if action == "promote_to_install":
        result["status"] = "ok"
        result["reason"] = "reintegrated_and_valid"

        failed_original = ""
        if original_bundle and os.path.exists(original_bundle):
            failed_original = original_bundle
        else:
            guess = FAILED_DIR / bundle_name
            if guess.exists():
                failed_original = str(guess.resolve())

        if failed_original and os.path.exists(failed_original):
            try:
                os.remove(failed_original)
                result["original_failed_removed"] = True
                result["original_bundle"] = failed_original
            except Exception as e:
                result["original_failed_removed"] = False
                result["original_failed_remove_error"] = str(e)
    else:
        result["status"] = "failed"
        result["reason"] = action or "inspection_rejected"

    write_json(REPORT_PATH, result)
    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Reintegrate repaired bundle into incoming lane.")
    parser.add_argument("--action-payload-json", default="", help="Raw JSON string")
    parser.add_argument("--repaired-bundle", default="", help="Path or filename under repaired_bundles")
    parser.add_argument("--family", default="unknown", help="Optional family")
    parser.add_argument("--original-bundle", default="", help="Original failed bundle path")
    args = parser.parse_args()

    if args.action_payload_json:
        try:
            payload = json.loads(args.action_payload_json)
        except Exception:
            payload = {}
    else:
        payload = {
            "repaired_bundle": args.repaired_bundle,
            "family": args.family,
            "original_bundle": args.original_bundle
        }

    result = reintegrate(payload)

    print(json.dumps({
        "status": result["status"],
        "output": str(REPORT_PATH),
        "result": result
    }, indent=2))


if __name__ == "__main__":
    main()

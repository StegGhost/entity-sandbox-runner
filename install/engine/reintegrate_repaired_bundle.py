import argparse
import json
import shutil
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

BRAIN_REPORTS = ROOT / "brain_reports"
INCOMING_DIR = ROOT / "incoming_bundles"
INSTALLED_DIR = ROOT / "installed_bundles"
FAILED_DIR = ROOT / "failed_bundles"
REPAIRED_DIR = ROOT / "repaired_bundles"

OUTPUT_PATH = BRAIN_REPORTS / "reintegrate_repaired_bundle_result.json"


def now_ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def parse_json_maybe(text: str):
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def run_step(cmd: list[str]) -> dict:
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
            "duration": round(time.time() - start, 3),
            "parsed_stdout": parse_json_maybe(proc.stdout.strip()),
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": round(time.time() - start, 3),
            "parsed_stdout": None,
        }


def resolve_path(value: str | None) -> Path | None:
    if not value:
        return None

    p = Path(value)
    if p.exists():
        return p.resolve()

    candidates = [
        ROOT / value,
        REPAIRED_DIR / value,
        FAILED_DIR / value,
        INCOMING_DIR / value,
        INSTALLED_DIR / value,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    return None


def load_action_payload(raw: str) -> dict:
    payload = json.loads(raw)
    if isinstance(payload, str):
        payload = json.loads(payload)
    if not isinstance(payload, dict):
        raise ValueError("action payload must be a JSON object")
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--action-payload-json", required=True)
    args = parser.parse_args()

    INCOMING_DIR.mkdir(parents=True, exist_ok=True)
    INSTALLED_DIR.mkdir(parents=True, exist_ok=True)
    FAILED_DIR.mkdir(parents=True, exist_ok=True)
    REPAIRED_DIR.mkdir(parents=True, exist_ok=True)
    BRAIN_REPORTS.mkdir(parents=True, exist_ok=True)

    try:
        payload = load_action_payload(args.action_payload_json)
    except Exception as e:
        result = {
            "status": "failed",
            "ts": now_ts(),
            "family": None,
            "repaired_bundle": None,
            "resolved_repaired_bundle": None,
            "incoming_bundle": None,
            "installed_bundle": None,
            "original_bundle": None,
            "original_failed_removed": False,
            "inspection_result": None,
            "reason": f"invalid_action_payload: {e}",
            "output_report": str(OUTPUT_PATH),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({
            "status": "failed",
            "output": str(OUTPUT_PATH),
            "result": result
        }, indent=2))
        return

    family = payload.get("family")
    repaired_bundle_value = payload.get("repaired_bundle") or payload.get("target")
    original_bundle_value = payload.get("original_bundle")

    repaired_bundle = resolve_path(repaired_bundle_value)
    original_bundle = resolve_path(original_bundle_value) if original_bundle_value else None

    if repaired_bundle is None or not repaired_bundle.exists():
        result = {
            "status": "failed",
            "ts": now_ts(),
            "family": family,
            "repaired_bundle": repaired_bundle_value,
            "resolved_repaired_bundle": None,
            "incoming_bundle": None,
            "installed_bundle": None,
            "original_bundle": str(original_bundle) if original_bundle else original_bundle_value,
            "original_failed_removed": False,
            "inspection_result": None,
            "reason": "missing_repaired_bundle",
            "output_report": str(OUTPUT_PATH),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({
            "status": "failed",
            "output": str(OUTPUT_PATH),
            "result": result
        }, indent=2))
        return

    incoming_bundle = INCOMING_DIR / repaired_bundle.name
    installed_bundle = INSTALLED_DIR / repaired_bundle.name

    if incoming_bundle.exists():
        incoming_bundle.unlink()

    shutil.copy2(repaired_bundle, incoming_bundle)

    inspect_step = run_step([
        "python",
        "install/engine/inspect_bundle_engine.py",
        "--action-payload-json",
        json.dumps({
            "action": "inspect_incoming_bundle_family",
            "target": str(incoming_bundle),
            "family": family,
        }),
    ])

    inspect_stdout = inspect_step.get("parsed_stdout") or {}
    inspection = inspect_stdout.get("inspection", {}) if isinstance(inspect_stdout, dict) else {}
    decision = inspection.get("decision", {}) if isinstance(inspection, dict) else {}

    decision_action = decision.get("action")
    decision_valid = decision.get("valid")

    promoted = False
    original_failed_removed = False

    if inspect_step["ok"] and decision_action == "promote_to_install" and decision_valid is True:
        if installed_bundle.exists():
            installed_bundle.unlink()
        shutil.move(str(incoming_bundle), str(installed_bundle))
        promoted = True

        if original_bundle and original_bundle.exists():
            original_bundle.unlink()
            original_failed_removed = True

        if repaired_bundle.exists():
            repaired_bundle.unlink()

        result = {
            "status": "ok",
            "ts": now_ts(),
            "family": family,
            "repaired_bundle": repaired_bundle_value,
            "resolved_repaired_bundle": str(repaired_bundle),
            "incoming_bundle": str(incoming_bundle),
            "installed_bundle": str(installed_bundle),
            "original_bundle": str(original_bundle) if original_bundle else original_bundle_value,
            "original_failed_removed": original_failed_removed,
            "inspection_result": inspect_step,
            "promoted": promoted,
            "reason": "promoted_to_install",
            "output_report": str(OUTPUT_PATH),
        }
        write_json(OUTPUT_PATH, result)
        print(json.dumps({
            "status": "ok",
            "output": str(OUTPUT_PATH),
            "result": result
        }, indent=2))
        return

    result = {
        "status": "failed",
        "ts": now_ts(),
        "family": family,
        "repaired_bundle": repaired_bundle_value,
        "resolved_repaired_bundle": str(repaired_bundle),
        "incoming_bundle": str(incoming_bundle),
        "installed_bundle": None,
        "original_bundle": str(original_bundle) if original_bundle else original_bundle_value,
        "original_failed_removed": False,
        "inspection_result": inspect_step,
        "promoted": False,
        "reason": "inspection_rejected",
        "output_report": str(OUTPUT_PATH),
    }
    write_json(OUTPUT_PATH, result)
    print(json.dumps({
        "status": "failed",
        "output": str(OUTPUT_PATH),
        "result": result
    }, indent=2))


if __name__ == "__main__":
    main()

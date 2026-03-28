import os
import json
import time
from pathlib import Path

ROOT = Path(os.getcwd())

FAILED_DIR = ROOT / "failed_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
BRAIN_REPORTS = ROOT / "brain_reports"

BRAIN_REPORTS.mkdir(exist_ok=True)

OUTPUT_PATH = BRAIN_REPORTS / "next_action.json"


def now_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def list_zip_files(path: Path):
    if not path.exists():
        return []
    return sorted([f for f in path.iterdir() if f.suffix == ".zip"])


def pick_next_action():
    failed = list_zip_files(FAILED_DIR)

    # 🔥 CRITICAL: always select ANY failed bundle
    if failed:
        target = str(failed[0].resolve())

        return {
            "status": "ready",
            "ts": now_ts(),
            "action": "repair_bundle",
            "family": "auto_detected",
            "target": target,
            "resolved_path": target,
            "reason": "repair_failed_bundle"
        }

    incoming = list_zip_files(INCOMING_DIR)

    if incoming:
        target = str(incoming[0].resolve())

        return {
            "status": "ready",
            "ts": now_ts(),
            "action": "inspect_bundle",
            "family": "incoming",
            "target": target,
            "resolved_path": target,
            "reason": "inspect_incoming"
        }

    return {
        "status": "idle",
        "ts": now_ts(),
        "action": None,
        "reason": "no_work"
    }


def main():
    result = pick_next_action()

    OUTPUT_PATH.write_text(json.dumps(result, indent=2))

    print(json.dumps({
        "status": result["status"],
        "output": str(OUTPUT_PATH),
        "result": result
    }, indent=2))


if __name__ == "__main__":
    main()

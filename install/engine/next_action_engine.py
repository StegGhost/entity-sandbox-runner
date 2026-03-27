import os
import json
import time
from pathlib import Path

ROOT = Path(os.getcwd())

FAILED_DIR = ROOT / "failed_bundles"
INCOMING_DIR = ROOT / "incoming_bundles"
BRAIN_REPORTS = ROOT / "brain_reports"

BRAIN_REPORTS.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = BRAIN_REPORTS / "next_action.json"


def now_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def list_bundles(path: Path):
    if not path.exists():
        return []
    return sorted([p for p in path.iterdir() if p.suffix == ".zip"])


def pick_failed_bundle():
    bundles = list_bundles(FAILED_DIR)
    if not bundles:
        return None
    return bundles[0]  # deterministic


def pick_incoming_bundle():
    bundles = list_bundles(INCOMING_DIR)
    if not bundles:
        return None
    return bundles[0]


def main():
    action = None

    # PRIORITY 1 → repair failed bundles
    failed = pick_failed_bundle()
    if failed:
        action = {
            "ts": now_ts(),
            "status": "ok",
            "selection_mode": "deterministic_failed_scan",
            "action_class": "repair",
            "action": "repair_bundle",
            "target": str(failed),
            "family": failed.stem,
            "priority": "high",
            "reason": "failed_bundle_present"
        }

    # PRIORITY 2 → inspect incoming bundles
    elif pick_incoming_bundle():
        incoming = pick_incoming_bundle()
        action = {
            "ts": now_ts(),
            "status": "ok",
            "selection_mode": "incoming_scan",
            "action_class": "inspect",
            "action": "inspect_bundle",
            "target": str(incoming),
            "family": incoming.stem,
            "priority": "medium",
            "reason": "incoming_bundle_present"
        }

    else:
        action = {
            "ts": now_ts(),
            "status": "idle",
            "reason": "no_work_available"
        }

    OUTPUT_PATH.write_text(json.dumps(action, indent=2))

    print(json.dumps({
        "status": action["status"],
        "output": str(OUTPUT_PATH),
        "next_action": action
    }, indent=2))


if __name__ == "__main__":
    main()

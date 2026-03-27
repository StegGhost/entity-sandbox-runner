import os
import json
import time
from typing import Dict, Any, List

ROOT = os.getcwd()

FAILED_DIR = os.path.join(ROOT, "failed_bundles")
INCOMING_DIR = os.path.join(ROOT, "incoming_bundles")
BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")

os.makedirs(BRAIN_REPORTS, exist_ok=True)

OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")


def now_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def list_bundles(path: str) -> List[str]:
    if not os.path.exists(path):
        return []
    return sorted([
        f for f in os.listdir(path)
        if f.endswith(".zip")
    ])


def select_failed_bundle() -> str:
    failed = list_bundles(FAILED_DIR)
    if not failed:
        return ""
    return failed[0]  # deterministic


def select_incoming_bundle() -> str:
    incoming = list_bundles(INCOMING_DIR)
    if not incoming:
        return ""
    return incoming[0]


def build_action() -> Dict[str, Any]:
    incoming_bundle = select_incoming_bundle()
    if incoming_bundle:
        return {
            "ts": now_ts(),
            "status": "ok",
            "selection_mode": "incoming_priority",
            "action_class": "inspection",
            "active_family": "auto",
            "action": "inspect_incoming_bundle_family",
            "target": os.path.join(INCOMING_DIR, incoming_bundle),
            "family": "auto",
            "priority": "high",
            "reason": "incoming_bundle_detected",
            "source": "next_action_engine"
        }

    failed_bundle = select_failed_bundle()
    if failed_bundle:
        return {
            "ts": now_ts(),
            "status": "ok",
            "selection_mode": "failed_priority",
            "action_class": "repair",
            "active_family": "auto",
            "action": "propose_repair_for_bundle_family",
            "target": failed_bundle,
            "family": "auto",
            "priority": "high",
            "reason": "failed_bundle_detected",
            "source": "next_action_engine"
        }

    return {
        "ts": now_ts(),
        "status": "ok",
        "selection_mode": "idle",
        "action_class": "idle",
        "active_family": "none",
        "action": "idle",
        "target": "",
        "family": "none",
        "priority": "low",
        "reason": "no_work",
        "source": "next_action_engine"
    }


def main():
    action = build_action()

    result = {
        "status": "ok",
        "output": OUTPUT_PATH,
        "next_action": action
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

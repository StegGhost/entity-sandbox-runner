import json
import os
from datetime import datetime

from install.engine.repo_snapshot import snapshot_repo_state

ROOT = os.getcwd()
BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")


def utc_now():
    return datetime.utcnow().isoformat()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_json(path, payload):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def choose_action(snapshot):
    incoming = snapshot.get("incoming_bundle_count", 0)
    failed = snapshot.get("failed_bundle_count", 0)

    # Priority 1: process incoming work
    if incoming > 0:
        return {
            "action": "process_incoming_bundle",
            "reason": "incoming_bundle_available",
            "priority": "high",
        }

    # Priority 2: retry failed bundles
    if failed > 0:
        return {
            "action": "requeue_failed_bundle",
            "reason": "failed_bundle_available",
            "priority": "medium",
        }

    # Priority 3: no work
    return {
        "action": "idle",
        "reason": "no_work_detected",
        "priority": "low",
    }


def main():
    ensure_dir(BRAIN_REPORTS)

    snapshot = snapshot_repo_state()

    decision = choose_action(snapshot)

    output = {
        "generated_at": utc_now(),
        "snapshot": {
            "incoming_bundle_count": snapshot.get("incoming_bundle_count"),
            "installed_bundle_count": snapshot.get("installed_bundle_count"),
            "failed_bundle_count": snapshot.get("failed_bundle_count"),
            "has_work": snapshot.get("has_work"),
            "cge_state": snapshot.get("cge_state"),
        },
        "next_action": {
            "ts": utc_now(),
            "status": "ok",
            "selection_mode": "snapshot_driven",
            "action": decision["action"],
            "target": None,
            "priority": decision["priority"],
            "reason": decision["reason"],
        },
    }

    write_json(OUTPUT_PATH, output)

    print(json.dumps({
        "status": "ok",
        "action": decision["action"],
        "incoming": snapshot.get("incoming_bundle_count"),
        "failed": snapshot.get("failed_bundle_count"),
    }, indent=2))


if __name__ == "__main__":
    main()

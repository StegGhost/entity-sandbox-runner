import json
import os
from datetime import datetime

ROOT = os.getcwd()
BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")

SNAPSHOT_PATH = os.path.join(BRAIN_REPORTS, "repo_snapshot.json")
RECONCILED_STATE_PATH = os.path.join(BRAIN_REPORTS, "reconciled_state.json")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")


def utc_now():
    return datetime.utcnow().isoformat()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_json(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, payload):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def choose_next_action(snapshot, reconciled):
    incoming_count = snapshot.get("incoming_bundle_count", 0)
    failed_count = snapshot.get("failed_bundle_count", 0)
    review_state = (reconciled.get("review") or {}).get("state")

    if incoming_count > 0:
        return {
            "ts": utc_now(),
            "status": "ok",
            "action": "process_incoming_bundle",
            "priority": "high",
            "reason": "incoming bundles are waiting",
        }

    if review_state in {"executed_pending_review", "pending_review"}:
        return {
            "ts": utc_now(),
            "status": "ok",
            "action": "await_settlement",
            "priority": "medium",
            "reason": f"previous execution still settling: {review_state}",
        }

    if failed_count > 0:
        return {
            "ts": utc_now(),
            "status": "ok",
            "action": "requeue_failed_bundle",
            "priority": "medium",
            "reason": "no incoming bundles; attempt failed-bundle recovery",
        }

    return {
        "ts": utc_now(),
        "status": "ok",
        "action": "idle",
        "priority": "low",
        "reason": "no admissible next action found",
    }


def main():
    ensure_dir(BRAIN_REPORTS)

    snapshot = load_json(SNAPSHOT_PATH, {})
    reconciled = load_json(RECONCILED_STATE_PATH, {})

    next_action = choose_next_action(snapshot, reconciled)

    output = {
        "generated_at": utc_now(),
        "snapshot_summary": {
            "repo_hash": snapshot.get("repo_hash"),
            "incoming_bundle_count": snapshot.get("incoming_bundle_count"),
            "installed_bundle_count": snapshot.get("installed_bundle_count"),
            "failed_bundle_count": snapshot.get("failed_bundle_count"),
            "last_review_state": snapshot.get("last_review_state"),
        },
        "reconciled_summary": {
            "review_state": (reconciled.get("review") or {}).get("state"),
            "review_reason": (reconciled.get("review") or {}).get("reason"),
        },
        "next_action": next_action,
    }

    write_json(OUTPUT_PATH, output)

    print(json.dumps({
        "status": "ok",
        "output": OUTPUT_PATH,
        "next_action": next_action,
    }, indent=2))


if __name__ == "__main__":
    main()

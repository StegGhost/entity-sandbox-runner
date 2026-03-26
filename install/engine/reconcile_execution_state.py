import json
import os
from datetime import datetime

ROOT = os.getcwd()

BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")

NEXT_ACTION_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")
EXECUTION_RESULT_PATH = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")
SNAPSHOT_PATH = os.path.join(BRAIN_REPORTS, "repo_snapshot.json")
OUTPUT_PATH = os.path.join(BRAIN_REPORTS, "reconciled_state.json")


def utc_now():
    return datetime.utcnow().isoformat()


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return default


def normalize_bundle_name(name):
    if not name:
        return None
    return os.path.basename(name)


def build_reconciled_state():
    next_doc = load_json(NEXT_ACTION_PATH, {})
    exec_doc = load_json(EXECUTION_RESULT_PATH, {})
    snapshot = load_json(SNAPSHOT_PATH, {})

    next_action = next_doc.get("next_action", {})
    execution = exec_doc.get("execution", {})

    selected_action = next_action.get("action")
    selected_reason = next_action.get("reason")

    execution_status = execution.get("status")
    execution_bundle = normalize_bundle_name(execution.get("bundle"))
    execution_family = execution.get("family")

    review_state = "unknown"
    review_reason = "insufficient_evidence"

    if selected_action == "idle":
        review_state = "idle"
        review_reason = "no_action_requested"
    elif selected_action == "await_settlement":
        review_state = "pending_review"
        review_reason = "awaiting_settlement"
    elif execution_status == "ok" and execution.get("action") == "process_incoming_bundle":
        review_state = "ingested"
        review_reason = "bundle_moved_to_installed"
    elif execution_status == "ok" and execution.get("action") == "requeue_failed_bundle":
        review_state = "executed_pending_review"
        review_reason = "bundle_requeued_to_incoming"
    elif execution_status == "failed":
        review_state = "failed"
        review_reason = execution.get("reason") or "execution_failed"

    state = {
        "generated_at": utc_now(),
        "selected": {
            "action": selected_action,
            "reason": selected_reason,
        },
        "execution": {
            "status": execution_status,
            "executed": execution.get("executed"),
            "action": execution.get("action"),
            "bundle": execution_bundle,
            "family": execution_family,
            "details": execution,
        },
        "snapshot": {
            "repo_hash": snapshot.get("repo_hash"),
            "incoming_bundle_count": snapshot.get("incoming_bundle_count"),
            "installed_bundle_count": snapshot.get("installed_bundle_count"),
            "failed_bundle_count": snapshot.get("failed_bundle_count"),
        },
        "review": {
            "state": review_state,
            "reason": review_reason,
            "bundle": execution_bundle,
            "family": execution_family,
        },
    }

    return state


def main():
    ensure_dir(BRAIN_REPORTS)
    reconciled = build_reconciled_state()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(reconciled, f, indent=2)
        f.write("\n")

    print(json.dumps({
        "status": "ok",
        "output": OUTPUT_PATH,
        "review_state": reconciled["review"]["state"],
        "bundle": reconciled["review"]["bundle"],
        "family": reconciled["review"]["family"],
    }, indent=2))


if __name__ == "__main__":
    main()

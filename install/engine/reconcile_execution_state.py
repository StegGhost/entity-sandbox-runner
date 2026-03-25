import json
import os
from datetime import datetime

ROOT = os.getcwd()

BRAIN_REPORTS = os.path.join(ROOT, "brain_reports")
LOGS = os.path.join(ROOT, "logs")

NEXT_ACTION_PATH = os.path.join(BRAIN_REPORTS, "next_action.json")
EXECUTION_RESULT_PATH = os.path.join(BRAIN_REPORTS, "execute_next_action_result.json")
INGESTION_LOG_PATH = os.path.join(LOGS, "ingestion_log.json")
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


def family_key(name):
    if not name:
        return None
    name = os.path.basename(name)
    if name.endswith(".zip"):
        name = name[:-4]
    for suffix in ["_manifest_fixed", "_fixed", "_bundle"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    if "_v" in name:
        name = name.split("_v")[0]
    return name


def load_ingestion_log():
    data = load_json(INGESTION_LOG_PATH, [])
    return data if isinstance(data, list) else []


def latest_ingestion_entry_for(bundle_name, log_entries):
    bundle_name = normalize_bundle_name(bundle_name)
    if not bundle_name:
        return None
    matches = [e for e in log_entries if normalize_bundle_name(e.get("bundle")) == bundle_name]
    if not matches:
        return None
    return sorted(matches, key=lambda e: e.get("ts", 0))[-1]


def build_reconciled_state():
    next_doc = load_json(NEXT_ACTION_PATH, {})
    exec_doc = load_json(EXECUTION_RESULT_PATH, {})
    ingestion_log = load_ingestion_log()

    next_action = next_doc.get("next_action", {})
    resolved = exec_doc.get("resolved_next_action", {}) or next_action
    execution = exec_doc.get("execution", {})
    ingestion = exec_doc.get("ingestion", {})

    selected_target = normalize_bundle_name(resolved.get("target"))
    selected_family = resolved.get("family") or family_key(selected_target)
    selected_action = resolved.get("action")

    execution_bundle = normalize_bundle_name(
        execution.get("bundle")
        or execution.get("repaired_bundle")
        or execution.get("target")
        or selected_target
    )

    log_match = latest_ingestion_entry_for(execution_bundle, ingestion_log)

    if log_match is None and execution_bundle and execution_bundle.endswith("_manifest_fixed.zip"):
        original = execution_bundle.replace("_manifest_fixed.zip", ".zip")
        log_match = latest_ingestion_entry_for(original, ingestion_log)

    state = {
        "generated_at": utc_now(),
        "selected": {
            "action": selected_action,
            "target": selected_target,
            "family": selected_family,
            "source": resolved.get("source") or next_action.get("source"),
            "priority": resolved.get("priority"),
            "reason": resolved.get("reason"),
        },
        "execution": {
            "status": execution.get("status"),
            "executed": execution.get("executed"),
            "action": execution.get("action") or selected_action,
            "bundle": execution_bundle,
            "details": execution,
        },
        "ingestion": {
            "trigger_status": ingestion.get("status"),
            "trigger_reason": ingestion.get("reason"),
            "log_match_found": log_match is not None,
            "latest_log_entry": log_match,
        },
        "review": {},
    }

    review_state = "unknown"
    review_reason = "insufficient_evidence"

    if log_match:
        if log_match.get("ok") is True:
            review_state = "ingested"
            review_reason = "ingestion_log_ok"
        else:
            review_state = "failed"
            review_reason = log_match.get("error") or "ingestion_log_failed"
    elif execution.get("status") == "failed":
        review_state = "failed"
        review_reason = execution.get("reason") or "execution_failed"
    elif ingestion.get("status") == "triggered":
        review_state = "pending_review"
        review_reason = "awaiting_ingestion_log"
    elif execution.get("status") == "ok":
        review_state = "executed_pending_review"
        review_reason = "execution_ok_no_ingestion_confirmation"

    state["review"] = {
        "state": review_state,
        "reason": review_reason,
        "bundle": execution_bundle,
        "family": selected_family,
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

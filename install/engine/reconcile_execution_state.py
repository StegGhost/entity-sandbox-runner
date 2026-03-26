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
            return json.load(f)
    except Exception:
        return default


def normalize(name):
    if not name:
        return None
    return os.path.basename(name)


def family_key(name):
    if not name:
        return None
    name = normalize(name)
    if name.endswith(".zip"):
        name = name[:-4]
    for suffix in ["_manifest_fixed", "_fixed", "_bundle"]:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    if "_v" in name:
        name = name.split("_v")[0]
    return name


def latest_ingestion_entry(bundle, log):
    bundle = normalize(bundle)
    matches = [e for e in log if normalize(e.get("bundle")) == bundle]
    if not matches:
        return None
    return sorted(matches, key=lambda x: x.get("ts", 0))[-1]


def main():
    ensure_dir(BRAIN_REPORTS)

    next_doc = load_json(NEXT_ACTION_PATH, {})
    exec_doc = load_json(EXECUTION_RESULT_PATH, {})
    ingestion_log = load_json(INGESTION_LOG_PATH, [])

    next_action = next_doc.get("next_action", {})
    execution = exec_doc.get("execution", {})
    ingestion = exec_doc.get("ingestion", {})

    target = normalize(next_action.get("target"))
    action = next_action.get("action")
    family = next_action.get("family") or family_key(target)

    execution_bundle = normalize(
        execution.get("bundle")
        or execution.get("repaired_bundle")
        or execution.get("target")
        or target
    )

    log_match = latest_ingestion_entry(execution_bundle, ingestion_log)

    # ---- CORE DECISION LOGIC ----
    if execution.get("status") == "failed":
        review_state = "failed"
        reason = execution.get("reason", "execution_failed")

    elif log_match:
        if log_match.get("ok") is True:
            review_state = "ingested"
            reason = "ingestion_success"
        else:
            review_state = "failed"
            reason = log_match.get("error", "ingestion_failed")

    elif ingestion.get("status") == "triggered":
        review_state = "pending"
        reason = "waiting_for_ingestion"

    elif execution.get("status") == "ok":
        review_state = "executed"
        reason = "execution_without_confirmation"

    else:
        review_state = "unknown"
        reason = "no_signal"

    # ---- OUTPUT ----
    result = {
        "generated_at": utc_now(),
        "selected": {
            "action": action,
            "target": target,
            "family": family,
        },
        "execution": {
            "status": execution.get("status"),
            "bundle": execution_bundle,
        },
        "ingestion": {
            "triggered": ingestion.get("status") == "triggered",
            "log_found": log_match is not None,
        },
        "review": {
            "state": review_state,
            "reason": reason,
            "bundle": execution_bundle,
            "family": family,
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    print(json.dumps({
        "status": "ok",
        "review_state": review_state,
        "bundle": execution_bundle,
        "family": family,
    }, indent=2))


if __name__ == "__main__":
    main()

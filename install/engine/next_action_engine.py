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


# 🔍 NEW — detect repo repair candidates
def detect_repo_issues(snapshot):
    issues = []

    # missing expected files (baseline sanity)
    expected_files = [
        "install/engine/execute_next_action.py",
        "install/engine/next_action_engine.py",
        "install/engine/reconcile_execution_state.py",
        "install/engine/repo_snapshot.py",
    ]

    existing = set(snapshot.get("files", []))

    for f in expected_files:
        if f not in existing:
            issues.append({
                "type": "missing_core_file",
                "target": f,
                "priority": "critical",
            })

    # bundle backlog
    if snapshot.get("incoming_bundle_count", 0) > 0:
        issues.append({
            "type": "incoming_bundle",
            "priority": "high",
        })

    if snapshot.get("failed_bundle_count", 0) > 0:
        issues.append({
            "type": "failed_bundle",
            "priority": "medium",
        })

    return issues


def choose_next_action(snapshot, reconciled):
    issues = detect_repo_issues(snapshot)

    if issues:
        top = issues[0]

        if top["type"] == "missing_core_file":
            return {
                "ts": utc_now(),
                "status": "ok",
                "action": "repair_repo_file",
                "target": top["target"],
                "priority": "critical",
                "reason": "missing core engine file",
            }

        if top["type"] == "incoming_bundle":
            return {
                "ts": utc_now(),
                "status": "ok",
                "action": "process_incoming_bundle",
                "priority": "high",
                "reason": "incoming bundles waiting",
            }

        if top["type"] == "failed_bundle":
            return {
                "ts": utc_now(),
                "status": "ok",
                "action": "requeue_failed_bundle",
                "priority": "medium",
                "reason": "failed bundles exist",
            }

    # fallback to stabilization
    return {
        "ts": utc_now(),
        "status": "ok",
        "action": "idle",
        "priority": "low",
        "reason": "no issues detected",
    }


def main():
    ensure_dir(BRAIN_REPORTS)

    snapshot = load_json(SNAPSHOT_PATH, {})
    reconciled = load_json(RECONCILED_STATE_PATH, {})

    next_action = choose_next_action(snapshot, reconciled)

    output = {
        "generated_at": utc_now(),
        "next_action": next_action,
        "snapshot_summary": {
            "repo_hash": snapshot.get("repo_hash"),
            "incoming": snapshot.get("incoming_bundle_count"),
            "failed": snapshot.get("failed_bundle_count"),
        }
    }

    write_json(OUTPUT_PATH, output)

    print(json.dumps({
        "status": "ok",
        "next_action": next_action,
    }, indent=2))


if __name__ == "__main__":
    main()

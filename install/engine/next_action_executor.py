import os
import json
import time
import subprocess

ROOT = os.getcwd()

NEXT_ACTION_PATH = os.path.join(ROOT, "brain_reports", "next_action.json")
RESULT_PATH = os.path.join(ROOT, "brain_reports", "execute_next_action_result.json")

def load_next_action():
    if not os.path.exists(NEXT_ACTION_PATH):
        return None
    with open(NEXT_ACTION_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def write_result(result):
    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

def execute(action):
    action_type = action.get("action")
    target = action.get("target")

    # Only supported action for now
    if action_type == "repair_bundle_manifest":
        return {
            "status": "ok",
            "executed": True,
            "action": action_type,
            "target": target,
            "note": "delegated to ingestion pipeline"
        }

    return {
        "status": "noop",
        "executed": False,
        "action": action_type,
        "target": target,
        "note": "unsupported action"
    }

def run():
    doc = load_next_action()

    if not doc:
        write_result({
            "status": "no_action",
            "executed": False
        })
        return

    next_action = doc.get("next_action", {})
    result = execute(next_action)

    output = {
        "ts": time.time(),
        "status": "ok",
        "action": next_action,
        "execution": result
    }

    write_result(output)

if __name__ == "__main__":
    run()
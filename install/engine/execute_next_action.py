import json
import os
from datetime import datetime

OUTPUT_PATH = "brain_reports/execute_next_action_result.json"
NEXT_ACTION_PATH = "brain_reports/next_action.json"


def ensure_dirs():
    os.makedirs("brain_reports", exist_ok=True)


def load_next_action():
    if not os.path.exists(NEXT_ACTION_PATH):
        return {
            "status": "error",
            "reason": "missing_next_action"
        }

    with open(NEXT_ACTION_PATH, "r") as f:
        return json.load(f)


def execute_action(action):
    # 🔧 Minimal safe execution layer (no side effects yet)
    return {
        "status": "ok",
        "executed": True,
        "action": action.get("action"),
        "target": action.get("target"),
        "note": "execution stub (no-op for now)"
    }


def main():
    ensure_dirs()

    ts = datetime.utcnow().isoformat()

    next_action = load_next_action()

    if next_action.get("status") == "error":
        result = {
            "ts": ts,
            "status": "failed",
            "reason": next_action.get("reason"),
        }
    else:
        execution = execute_action(next_action)

        result = {
            "ts": ts,
            "status": execution["status"],
            "action": next_action,
            "execution": execution
        }

    # 🔴 THIS is what was missing before
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

import json
import os
from typing import Any, Dict

ROOT = os.getcwd()

NEXT_ACTION_PATH = os.path.join(ROOT, "brain_reports", "next_action.json")
EXECUTION_RESULT_PATH = os.path.join(ROOT, "brain_reports", "execute_next_action_result.json")


def load_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: str, payload: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def handle_repair(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    from install.engine.repair_bundle_engine import propose_repair

    result = propose_repair(action_payload)

    return {
        "status": "ok" if result.get("status") == "ok" else "failed",
        "action": "repair_bundle",
        "result": result
    }


def execute_action(action: Dict[str, Any]) -> Dict[str, Any]:
    action_type = action.get("action")

    if action_type == "propose_repair_for_bundle_family":
        return handle_repair(action)

    return {
        "status": "ok",
        "executed": False,
        "action": "idle",
        "reason": "no_action_handler"
    }


def main():
    payload = load_json(NEXT_ACTION_PATH)

    next_action = payload.get("next_action", {})

    if not next_action:
        result = {
            "status": "ok",
            "executed": False,
            "reason": "no_next_action"
        }
        write_json(EXECUTION_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    execution = execute_action(next_action)

    result = {
        "status": "ok",
        "executed": True,
        "execution": execution
    }

    write_json(EXECUTION_RESULT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

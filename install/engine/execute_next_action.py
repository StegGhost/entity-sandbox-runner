import json
import os
import sys
from pathlib import Path
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from steggate import validate_and_execute, issue_token

ROOT = Path(__file__).resolve().parents[2]
BRAIN_REPORTS = ROOT / "brain_reports"
NEXT_ACTION_PATH = BRAIN_REPORTS / "next_action.json"
EXECUTION_RESULT_PATH = BRAIN_REPORTS / "execution_result.json"


def load_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp_path.replace(path)


def build_governed_test_action(next_action: dict) -> dict:
    """
    Convert the loop's selected action into a minimal governed HTTP action.

    This gives the loop one real execution path that can be validated,
    receipted, and reconciled immediately.
    """
    action_name = next_action.get("action", "unknown")
    target_ref = next_action.get("target")
    family = next_action.get("family")
    reason = next_action.get("reason")

    return {
        "type": "http_request",
        "target": "https://httpbin.org/post",
        "payload": {
            "source": "execute_next_action",
            "selected_action": action_name,
            "selected_target": target_ref,
            "family": family,
            "reason": reason,
            "ts": datetime.utcnow().isoformat()
        }
    }


def execute_next_action(action: dict):
    try:
        token_obj = issue_token()
        token = token_obj["token"]

        result = validate_and_execute(
            action=action.get("type"),
            target=action.get("target"),
            payload=action.get("payload", {}),
            token=token
        )

        return {
            "status": "ok",
            "execution": result,
            "input_action": action
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "input_action": action
        }


def main():
    next_action_payload = load_json(NEXT_ACTION_PATH)

    if not next_action_payload:
        result = {
            "status": "failed",
            "reason": "missing_next_action_payload",
            "output": str(EXECUTION_RESULT_PATH)
        }
        write_json(EXECUTION_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    next_action = next_action_payload.get("next_action", {})
    selected_action = next_action.get("action", "idle")

    if selected_action == "idle":
        result = {
            "status": "ok",
            "executed": False,
            "reason": "idle_no_op",
            "output": str(EXECUTION_RESULT_PATH)
        }
        write_json(EXECUTION_RESULT_PATH, result)
        print(json.dumps(result, indent=2))
        return

    governed_action = build_governed_test_action(next_action)
    execution = execute_next_action(governed_action)

    result = {
        "status": "ok" if execution.get("status") == "ok" else "failed",
        "output": str(EXECUTION_RESULT_PATH),
        "selected_next_action": next_action,
        "governed_action": governed_action,
        "execution_result": execution
    }

    write_json(EXECUTION_RESULT_PATH, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

import sys
import os

# Ensure local path works regardless of execution context
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from steggate import validate_and_execute, issue_token


def execute_next_action(action):
    """
    Expected action format:
    {
        "type": "http_request",
        "target": "...",
        "payload": {...}
    }
    """

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
            "execution": result
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "action": action
        }

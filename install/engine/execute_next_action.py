import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]

NEXT_ACTION_PATH = ROOT / "brain_reports" / "next_action.json"
EXECUTION_RESULT_PATH = ROOT / "brain_reports" / "execute_next_action_result.json"


def load_next_action():
    if not NEXT_ACTION_PATH.exists():
        return None

    try:
        return json.loads(NEXT_ACTION_PATH.read_text())
    except Exception:
        return None


def execute_action(action: dict):
    if not action:
        return {
            "status": "failed",
            "reason": "no_action"
        }

    action_type = action.get("action")

    if action_type == "propose_repair_for_bundle_family":
        return handle_repair(action)

    return {
        "status": "failed",
        "reason": f"unknown_action:{action_type}"
    }


def handle_repair(action):
    try:
        from install.engine.repair_bundle_engine import propose_repair
    except Exception as e:
        return {
            "status": "failed",
            "reason": f"import_error:{str(e)}"
        }

    try:
        result = propose_repair(action)
        return {
            "status": "ok",
            "action": "repair_bundle",
            "result": result
        }
    except Exception as e:
        return {
            "status": "failed",
            "reason": f"repair_failed:{str(e)}"
        }


def persist_execution_result(payload: dict):
    EXECUTION_RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)

    EXECUTION_RESULT_PATH.write_text(
        json.dumps(payload, indent=2)
    )


def main():
    next_action_data = load_next_action()

    if not next_action_data:
        output = {
            "status": "failed",
            "reason": "no_next_action"
        }
        print(json.dumps(output, indent=2))
        return

    next_action = next_action_data.get("next_action")

    execution = execute_action(next_action)

    payload = {
        "status": "ok",
        "executed": True,
        "timestamp": datetime.utcnow().isoformat(),
        "execution": execution
    }

    # 🔥 CRITICAL FIX: ALWAYS persist BEFORE printing
    persist_execution_result(payload)

    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

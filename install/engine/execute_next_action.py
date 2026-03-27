import json
import os
import sys

# --- SAFE IMPORT PATH ---
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# --- IMPORT ENGINES ---
from install.engine.repair_bundle_engine import propose_repair

OUTPUT_PATH = "brain_reports/execute_next_action_result.json"


def _write_output(data):
    os.makedirs("brain_reports", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)


def execute(action_payload):
    action = action_payload.get("action")

    result = {
        "status": "ok",
        "executed": False,
        "action": action,
        "reason": None
    }

    try:
        if action == "propose_repair_for_bundle_family":
            repair_result = propose_repair(action_payload)

            result.update({
                "executed": True,
                "repair": repair_result
            })

        elif action == "inspect_failed_bundle_family":
            # passive action
            result.update({
                "executed": False,
                "reason": "inspection_only"
            })

        else:
            result.update({
                "executed": False,
                "reason": "no_action_handler"
            })

    except Exception as e:
        result.update({
            "executed": False,
            "reason": str(e)
        })

    _write_output(result)
    return result


if __name__ == "__main__":
    # expects next_action.json
    with open("brain_reports/next_action.json", "r") as f:
        payload = json.load(f)

    execute(payload["next_action"])

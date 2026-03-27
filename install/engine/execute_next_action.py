import json
import os
from datetime import datetime

# --- Import repair engine ---
try:
    from install.engine.repair_engine_v1 import propose_repair
except Exception:
    propose_repair = None


OUTPUT_PATH = "brain_reports/execute_next_action_result.json"


def _write_output(data):
    os.makedirs("brain_reports", exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)


def execute(action_payload):
    ts = datetime.utcnow().isoformat()

    if not action_payload or not action_payload.get("action"):
        result = {
            "status": "ok",
            "executed": False,
            "action": "idle",
            "reason": "no_action_to_execute",
            "ts": ts
        }
        _write_output(result)
        return result

    action = action_payload["action"]

    # --- HANDLE REPAIR ACTION ---
    if action == "propose_repair_for_bundle_family":
        if propose_repair is None:
            result = {
                "status": "failed",
                "executed": False,
                "action": action,
                "reason": "repair_engine_not_available",
                "ts": ts
            }
        else:
            repair_result = propose_repair(action_payload)

            result = {
                "status": "ok",
                "executed": True,
                "action": action,
                "repair": repair_result,
                "ts": ts
            }

        _write_output(result)
        return result

    # --- DEFAULT FALLBACK ---
    result = {
        "status": "ok",
        "executed": False,
        "action": action,
        "reason": "no_action_handler",
        "ts": ts
    }

    _write_output(result)
    return result


if __name__ == "__main__":
    path = "brain_reports/next_action.json"
    if os.path.exists(path):
        with open(path) as f:
            payload = json.load(f)
    else:
        payload = {}

    execute(payload)

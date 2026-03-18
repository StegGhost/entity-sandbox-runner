import json
import os
from install.safe_json import list_valid_json_files, safe_load_json

def record_cycle(state, results, action, u):
    os.makedirs("payload/replay", exist_ok=True)
    with open(f"payload/replay/c_{state['cycles']:04d}.json", "w") as f:
        json.dump({"state": state, "results": results, "action": action, "u": u}, f, indent=2)

def load_replay_history():
    history = []
    for full in list_valid_json_files("payload/replay"):
        payload = safe_load_json(full)
        if payload is not None:
            history.append(payload)
    return history

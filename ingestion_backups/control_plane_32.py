import json
import os

CONTROL_PLANE_PATH = "payload/control_plane/override.json"

def load_control_plane_override():
    if not os.path.exists(CONTROL_PLANE_PATH):
        return None
    if os.path.getsize(CONTROL_PLANE_PATH) == 0:
        return None
    try:
        with open(CONTROL_PLANE_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return None

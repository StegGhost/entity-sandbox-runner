import json
import os

def safe_load_json(path):
    if not path.endswith(".json"):
        return None
    if not os.path.exists(path):
        return None
    if os.path.getsize(path) == 0:
        return None
    with open(path, "r") as f:
        return json.load(f)

def list_valid_json_files(directory):
    if not os.path.exists(directory):
        return []
    out = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        full = os.path.join(directory, name)
        if not os.path.isfile(full):
            continue
        if os.path.getsize(full) == 0:
            continue
        out.append(full)
    return out

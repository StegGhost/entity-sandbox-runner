
import json
from pathlib import Path

PATH = Path("config/stake_registry.json")

def load():
    if not PATH.exists():
        return {}
    return json.loads(PATH.read_text())

def save(data):
    PATH.parent.mkdir(parents=True, exist_ok=True)
    PATH.write_text(json.dumps(data, indent=2))

def set_stake(node_id, amount):
    data = load()
    data[node_id] = amount
    save(data)

def get_stake(node_id):
    return load().get(node_id, 0)

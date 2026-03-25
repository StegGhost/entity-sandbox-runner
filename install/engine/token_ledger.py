
import json
from pathlib import Path

LEDGER = Path("config/token_ledger.json")

def load():
    if not LEDGER.exists():
        return {}
    return json.loads(LEDGER.read_text())

def save(data):
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(data, indent=2))

def get_balance(node_id):
    return load().get(node_id, 0)

def mint(node_id, amount):
    data = load()
    data[node_id] = data.get(node_id, 0) + amount
    save(data)

def burn(node_id, amount):
    data = load()
    data[node_id] = max(0, data.get(node_id, 0) - amount)
    save(data)

def transfer(from_id, to_id, amount):
    data = load()
    if data.get(from_id, 0) < amount:
        return False
    data[from_id] -= amount
    data[to_id] = data.get(to_id, 0) + amount
    save(data)
    return True

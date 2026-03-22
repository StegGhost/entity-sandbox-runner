
import json
from pathlib import Path

STAKE = Path("config/stake_registry.json")
LEDGER = Path("logs/rewards_ledger.json")

def load(p):
    if not p.exists():
        return {}
    return json.loads(p.read_text())

def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2))

def adjust_stake(node_id, delta):
    data = load(STAKE)
    data[node_id] = max(0, data.get(node_id, 0) + delta)
    save(STAKE, data)

def reward(node_id, amount=5):
    adjust_stake(node_id, amount)
    record(node_id, "reward", amount)

def slash(node_id, amount=10):
    adjust_stake(node_id, -amount)
    record(node_id, "slash", amount)

def record(node_id, action, amount):
    data = []
    if LEDGER.exists():
        data = json.loads(LEDGER.read_text())
    data.append({
        "node": node_id,
        "action": action,
        "amount": amount
    })
    LEDGER.write_text(json.dumps(data, indent=2))

def process_votes(bundle_hash, votes, accepted):
    for node, decision in votes.items():
        if decision == "approve" and accepted:
            reward(node)
        elif decision == "approve" and not accepted:
            slash(node)
        elif decision == "reject" and accepted:
            slash(node)
        elif decision == "reject" and not accepted:
            reward(node)

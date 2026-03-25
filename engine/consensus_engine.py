
import json
from pathlib import Path

STATE = Path("logs/consensus_state.json")

def load_state():
    if not STATE.exists():
        return {"votes": {}}
    return json.loads(STATE.read_text())

def save_state(state):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))

def submit_vote(bundle_hash, node_id, decision):
    state = load_state()
    state["votes"].setdefault(bundle_hash, {})
    state["votes"][bundle_hash][node_id] = decision
    save_state(state)
    return state

def tally_votes(bundle_hash, threshold=2):
    state = load_state()
    votes = state["votes"].get(bundle_hash, {})
    approvals = sum(1 for v in votes.values() if v == "approve")
    if approvals >= threshold:
        return {"consensus": True, "approvals": approvals}
    return {"consensus": False, "approvals": approvals}

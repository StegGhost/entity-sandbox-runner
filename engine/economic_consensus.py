
from engine.stake_registry import get_stake
from engine.consensus_engine import load_state

def weighted_tally(bundle_hash, threshold=100):
    state = load_state()
    votes = state.get("votes", {}).get(bundle_hash, {})

    total = 0
    for node, decision in votes.items():
        if decision == "approve":
            total += get_stake(node)

    if total >= threshold:
        return {"consensus": True, "stake": total}

    return {"consensus": False, "stake": total}

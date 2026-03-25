
from engine.token_staking import get_stake
from engine.consensus_engine import load_state

def token_weighted_tally(bundle_hash, threshold=100):
    state = load_state()
    votes = state.get("votes", {}).get(bundle_hash, {})

    total = 0
    for node, decision in votes.items():
        if decision == "approve":
            total += get_stake(node)

    if total >= threshold:
        return {"consensus": True, "token_weight": total}

    return {"consensus": False, "token_weight": total}

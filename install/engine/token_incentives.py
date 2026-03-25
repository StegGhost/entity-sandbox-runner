
from engine.token_ledger import mint, burn
from engine.consensus_engine import load_state

def apply_token_incentives(bundle_hash, accepted):
    state = load_state()
    votes = state.get("votes", {}).get(bundle_hash, {})

    for node, decision in votes.items():
        if decision == "approve" and accepted:
            mint(node, 10)
        elif decision == "approve" and not accepted:
            burn(node, 5)
        elif decision == "reject" and accepted:
            burn(node, 5)
        elif decision == "reject" and not accepted:
            mint(node, 10)

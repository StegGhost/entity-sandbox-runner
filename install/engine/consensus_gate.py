
from engine.consensus_engine import tally_votes

def enforce_consensus(bundle_hash):
    result = tally_votes(bundle_hash)
    if not result.get("consensus"):
        return {"valid": False, "reason": "no_consensus", "approvals": result.get("approvals")}
    return {"valid": True}


from engine.economic_consensus import weighted_tally
import hashlib, json

def enforce_economic_consensus(manifest):
    h = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    result = weighted_tally(h)

    if not result.get("consensus"):
        return {
            "valid": False,
            "reason": "economic_consensus_failed",
            "stake": result.get("stake")
        }

    return {"valid": True, "stake": result.get("stake")}

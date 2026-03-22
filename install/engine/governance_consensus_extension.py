
from engine.consensus_gate import enforce_consensus
import hashlib, json

def apply_consensus(manifest):
    h = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
    result = enforce_consensus(h)
    if not result.get("valid"):
        return {"valid": False, "stage": "consensus", "reason": result}
    return {"valid": True}

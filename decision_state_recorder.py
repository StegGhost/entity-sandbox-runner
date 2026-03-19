import hashlib
import json
import time

def hash_data(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def record_decision(proposal, result, u_value, decision, authority):
    timestamp = time.time()

    state_snapshot = {
        "proposal": proposal.get("name"),
        "u": u_value,
        "decision": decision["action"]
    }

    receipt = {
        "timestamp": timestamp,
        "proposal": proposal.get("name"),
        "result": result,
        "u_value": u_value,
        "decision": decision,
        "authority": authority,
        "state_snapshot_hash": hash_data(state_snapshot),
        "constraint_vector": {
            "u_threshold": decision.get("threshold"),
            "stability_class": decision.get("class")
        }
    }

    receipt["receipt_hash"] = hash_data(receipt)

    return receipt

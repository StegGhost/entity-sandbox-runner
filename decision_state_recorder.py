import json, os, time, hashlib

def _hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def record_decision(proposal, result, u_value, decision, authority, previous_receipt_hash, receipt_dir):
    os.makedirs(receipt_dir, exist_ok=True)

    receipt = {
        "schema_version": "2.0.0",
        "timestamp": time.time(),
        "proposal": proposal.get("name"),
        "result": result,
        "u_value": u_value,
        "decision": decision,
        "authority": authority,
        "previous_receipt_hash": previous_receipt_hash
    }

    receipt["receipt_hash"] = _hash(receipt)

    filename = f"{int(receipt['timestamp'])}_{receipt['receipt_hash'][:10]}.json"
    path = os.path.join(receipt_dir, filename)

    with open(path, "w") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)

    receipt["receipt_path"] = path
    return receipt
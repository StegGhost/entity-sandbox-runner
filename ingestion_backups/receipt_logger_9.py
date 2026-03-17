import json, os, time, hashlib

def write_receipt(receipt_dir, state, results, summary):
    os.makedirs(receipt_dir, exist_ok=True)
    payload = {
        "ts": time.time(),
        "cycle": state.get("cycles"),
        "results": results,
        "summary": summary,
        "last_action": state.get("last_action"),
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
    payload["receipt_hash"] = digest
    path = os.path.join(receipt_dir, f"receipt_{state.get('cycles', 0):04d}.json")
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    return path

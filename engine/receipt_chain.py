import json
import hashlib
import os
import time

CHAIN_FILE = "receipt_chain.json"

def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def hash_data(data):
    return hashlib.sha256(canonical_json(data).encode()).hexdigest()

def load_chain():
    if not os.path.exists(CHAIN_FILE):
        return []
    with open(CHAIN_FILE, "r") as f:
        return json.load(f)

def save_chain(chain):
    with open(CHAIN_FILE, "w") as f:
        json.dump(chain, f, indent=2)

def append_receipt(passport_hash, action, result):
    chain = load_chain()
    prev_hash = chain[-1]["receipt_hash"] if chain else "GENESIS"

    receipt = {
        "timestamp": time.time(),
        "passport_hash": passport_hash,
        "action": action,
        "result": result,
        "previous_hash": prev_hash
    }

    receipt_hash = hash_data(receipt)
    receipt["receipt_hash"] = receipt_hash

    chain.append(receipt)
    save_chain(chain)

    return receipt

def verify_chain():
    chain = load_chain()
    prev = "GENESIS"

    for r in chain:
        expected_hash = hash_data({
            "timestamp": r["timestamp"],
            "passport_hash": r["passport_hash"],
            "action": r["action"],
            "result": r["result"],
            "previous_hash": r["previous_hash"]
        })

        if r["receipt_hash"] != expected_hash:
            return False, "hash_mismatch"

        if r["previous_hash"] != prev:
            return False, "chain_break"

        prev = r["receipt_hash"]

    return True, "valid"

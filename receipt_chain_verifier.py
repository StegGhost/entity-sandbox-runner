import os, json, hashlib

LOCK_FILE = ".chain_lock"

def _hash(data):
    data = dict(data)
    data.pop("receipt_hash", None)
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

def verify_chain(receipt_dir):
    if not os.path.exists(receipt_dir):
        return {"valid": True}

    files = sorted([f for f in os.listdir(receipt_dir) if f.endswith(".json")])
    prev = None

    for i, f in enumerate(files):
        with open(os.path.join(receipt_dir, f)) as fp:
            r = json.load(fp)

        if r.get("receipt_hash") != _hash(r):
            open(LOCK_FILE, "w").write("LOCKED")
            return {"valid": False, "reason": f"hash mismatch at index {i}"}

        if i > 0 and r.get("previous_receipt_hash") != prev:
            open(LOCK_FILE, "w").write("LOCKED")
            return {"valid": False, "reason": f"chain break at index {i}"}

        prev = r.get("receipt_hash")

    return {"valid": True}

def is_chain_locked():
    return os.path.exists(LOCK_FILE)

def clear_chain_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
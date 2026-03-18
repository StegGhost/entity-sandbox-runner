import json
import os
import hashlib

RECEIPT_DIR = "payload/receipts"

def safe_load(path):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return None
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def hash_payload(payload):
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()

def validate_and_repair(receipt_dir=RECEIPT_DIR):
    if not os.path.exists(receipt_dir):
        return []

    files = sorted([f for f in os.listdir(receipt_dir) if f.endswith(".json")])
    prev_hash = None
    repairs = []

    for f in files:
        full = os.path.join(receipt_dir, f)
        data = safe_load(full)

        if data is None:
            try:
                os.remove(full)
                repairs.append({"file": f, "action": "deleted_invalid"})
            except Exception:
                pass
            continue

        payload_copy = dict(data)
        expected_hash = payload_copy.pop("hash", None)
        payload_copy.pop("signature", None)

        actual_hash = hash_payload(payload_copy)
        if expected_hash != actual_hash:
            data["hash"] = actual_hash
            repairs.append({"file": f, "action": "rehash"})

        if prev_hash and data.get("prev_hash") != prev_hash:
            data["prev_hash"] = prev_hash
            repairs.append({"file": f, "action": "relink"})

        with open(full, "w") as out:
            json.dump(data, out, indent=2)

        prev_hash = data.get("hash")

    return repairs

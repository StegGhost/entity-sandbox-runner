import os
import json
import hashlib

RECEIPT_DIR = "payload/receipts"


def safe_load(path):
    try:
        if not os.path.exists(path):
            return None
        if os.path.getsize(path) == 0:
            return None
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def hash_payload(payload):
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def validate_and_repair():
    if not os.path.exists(RECEIPT_DIR):
        return []

    files = sorted([f for f in os.listdir(RECEIPT_DIR) if f.endswith(".json")])

    cleaned = []
    prev_hash = None
    repairs = []

    for f in files:
        full = os.path.join(RECEIPT_DIR, f)
        data = safe_load(full)

        if data is None:
            os.remove(full)
            repairs.append({"file": f, "action": "deleted_invalid"})
            continue

        # Check hash integrity
        expected_hash = data.get("hash")
        payload_copy = dict(data)
        payload_copy.pop("hash", None)
        payload_copy.pop("signature", None)

        actual_hash = hash_payload(payload_copy)

        if expected_hash != actual_hash:
            repairs.append({"file": f, "action": "rehash"})
            data["hash"] = actual_hash

        # Fix prev_hash chain
        if prev_hash and data.get("prev_hash") != prev_hash:
            repairs.append({"file": f, "action": "relink"})
            data["prev_hash"] = prev_hash

        # Rewrite repaired file
        with open(full, "w") as out:
            json.dump(data, out, indent=2)

        prev_hash = data.get("hash")
        cleaned.append(f)

    return repairs

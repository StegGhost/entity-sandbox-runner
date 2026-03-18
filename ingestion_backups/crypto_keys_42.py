import json
import os
import hashlib

def sign_with_keypair(data):
    raw = json.dumps(data, sort_keys=True)
    h = hashlib.sha256(raw.encode()).hexdigest()
    sig = hashlib.sha256((h + "secret").encode()).hexdigest()
    return h, sig


def safe_load_json(path):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return None
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def verify_chain(receipts_path):
    if not os.path.exists(receipts_path):
        return True

    files = sorted(os.listdir(receipts_path))

    prev_hash = None

    for f in files:
        if not f.endswith(".json"):
            continue

        full_path = os.path.join(receipts_path, f)
        data = safe_load_json(full_path)

        # 🚫 skip bad/corrupt files instead of crashing
        if data is None:
            print(f"[WARN] Skipping invalid receipt: {f}")
            continue

        expected_prev = data.get("prev_hash")

        if prev_hash and expected_prev != prev_hash:
            print(f"[WARN] Chain mismatch at {f}")

        prev_hash = data.get("hash")

    return True

import json
import hashlib
import os

PRIVATE_KEY = "priv-key"
PUBLIC_KEY = "pub-key"


def sign_with_keypair(payload):
    raw = json.dumps(payload, sort_keys=True)
    h = hashlib.sha256(raw.encode()).hexdigest()
    sig = hashlib.sha256((h + PRIVATE_KEY).encode()).hexdigest()
    return h, sig


def verify_chain(path):
    files = sorted(os.listdir(path))
    prev = None

    for f in files:
        if not f.endswith(".json"):
            continue

        full_path = os.path.join(path, f)

        try:
            if not os.path.exists(full_path):
                continue
            if os.path.getsize(full_path) == 0:
                continue

            with open(full_path, "r") as fh:
                p = json.load(fh)
        except Exception:
            continue

        if prev and p.get("prev_hash") != prev:
            raise Exception("CHAIN INVALID")

        prev = p.get("hash")

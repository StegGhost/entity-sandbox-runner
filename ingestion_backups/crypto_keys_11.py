import json
import hashlib
from install.safe_json import safe_load_json, list_valid_json_files

PRIVATE_KEY = "priv-key"
PUBLIC_KEY = "pub-key"

def sign_with_keypair(payload):
    raw = json.dumps(payload, sort_keys=True)
    h = hashlib.sha256(raw.encode()).hexdigest()
    sig = hashlib.sha256((h + PRIVATE_KEY).encode()).hexdigest()
    return h, sig

def verify_chain(path):
    files = list_valid_json_files(path)
    prev = None
    for full in files:
        payload = safe_load_json(full)
        if payload is None:
            continue
        if prev and payload.get("prev_hash") != prev:
            raise Exception("CHAIN INVALID")
        prev = payload.get("hash")

import hashlib
import json

def hash_receipt(r):
    raw = json.dumps(r, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def build_receipt(prev_hash, payload):
    r = dict(payload)
    r["prev_hash"] = prev_hash
    r["hash"] = hash_receipt(r)
    return r

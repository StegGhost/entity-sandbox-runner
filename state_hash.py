import json
import hashlib


def compute_state_hash(state):
    encoded = json.dumps(state, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()

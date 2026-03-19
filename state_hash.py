import hashlib
import json


def compute_state_hash(state):
    return hashlib.sha256(
        json.dumps(state, sort_keys=True, default=str).encode()
    ).hexdigest()

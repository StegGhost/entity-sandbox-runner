import json
import hashlib
from typing import Any


def compute_state_hash(state: Any) -> str:
    encoded = json.dumps(state, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

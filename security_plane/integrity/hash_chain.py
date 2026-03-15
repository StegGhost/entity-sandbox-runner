import json
import hashlib

def hash_event(event: dict, previous_hash: str | None = None) -> dict:
    payload = {
        "previous_hash": previous_hash,
        "event": event
    }
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
    payload["hash"] = digest
    return payload

def verify_chain(chain: list[dict]) -> bool:
    previous = None
    for item in chain:
        event = item["event"]
        expected = hash_event(event, previous)
        if expected["hash"] != item["hash"]:
            return False
        previous = item["hash"]
    return True

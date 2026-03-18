import json
import os

REGISTRY_PATH = "payload/network/peers.json"

def load_peers():
    if not os.path.exists(REGISTRY_PATH):
        return []
    if os.path.getsize(REGISTRY_PATH) == 0:
        return []
    try:
        with open(REGISTRY_PATH, "r") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def get_peer_receipts():
    peers = load_peers()
    receipts = []

    for p in peers:
        try:
            if not isinstance(p, str):
                continue
            if not os.path.exists(p):
                continue
            if os.path.getsize(p) == 0:
                continue
            if not p.endswith(".json"):
                continue
            with open(p, "r") as f:
                receipts.append(json.load(f))
        except Exception:
            continue

    return receipts

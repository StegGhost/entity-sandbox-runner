import json
import os

REGISTRY_PATH = "payload/network/peers.json"

def load_peers():
    if not os.path.exists(REGISTRY_PATH):
        return []
    try:
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)
    except:
        return []

def get_peer_receipts():
    peers = load_peers()
    receipts = []

    for p in peers:
        try:
            if os.path.exists(p):
                with open(p, "r") as f:
                    receipts.append(json.load(f))
        except:
            continue

    return receipts

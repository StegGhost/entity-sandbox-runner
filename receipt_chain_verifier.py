import os
import json
import hashlib


RECEIPT_DIR = "receipts"


def _hash(data):
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, default=str).encode()
    ).hexdigest()


def _load_receipts():
    if not os.path.isdir(RECEIPT_DIR):
        return []

    files = sorted([
        f for f in os.listdir(RECEIPT_DIR)
        if f.endswith(".json")
    ])

    receipts = []

    for f in files:
        path = os.path.join(RECEIPT_DIR, f)
        with open(path, "r") as file:
            receipts.append(json.load(file))

    return receipts

def verify_chain():
    receipts = _load_receipts()

    if not receipts:
        return True, "empty_chain"

    for i in range(len(receipts)):
        r = receipts[i]

        # 🔷 ALWAYS verify internal hash (even genesis)
        expected_hash = r.get("receipt_hash")
        recalculated = _hash({
            k: v for k, v in r.items() if k != "receipt_hash"
        })

        if expected_hash != recalculated:
            return False, f"hash mismatch at index {i}"

        # 🔷 Only enforce linkage if multiple receipts exist
        if i > 0:
            prev = receipts[i - 1]
            if r.get("previous_receipt_hash") != prev.get("receipt_hash"):
                return False, f"chain break at index {i}"

    return True, "chain valid"

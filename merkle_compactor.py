import hashlib
import json


def hash_pair(a, b):
    return hashlib.sha256((a + b).encode()).hexdigest()


def merkle_root(hashes):
    if not hashes:
        return None

    current = hashes[:]

    while len(current) > 1:
        next_layer = []

        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i + 1] if i + 1 < len(current) else left
            next_layer.append(hash_pair(left, right))

        current = next_layer

    return current[0]


def compact_receipts(receipts):
    hashes = [r["receipt_hash"] for r in receipts]

    return {
        "segment_root": merkle_root(hashes),
        "count": len(receipts),
        "proof_type": "merkle"
    }

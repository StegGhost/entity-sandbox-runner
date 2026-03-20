import os
import json
import hashlib


def compute_receipt_hash(receipt):
    data = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    encoded = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def _load_receipts(receipt_dir):
    if not os.path.exists(receipt_dir):
        return []

    receipts = []

    for fname in os.listdir(receipt_dir):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(receipt_dir, fname)

        with open(path, "r") as f:
            receipt = json.load(f)

        receipts.append(receipt)

    return receipts


def _order_receipts_by_chain(receipts):
    if not receipts:
        return []

    by_prev = {}
    genesis = None

    for r in receipts:
        prev = r.get("previous_receipt_hash")

        if prev is None:
            if genesis is not None:
                raise ValueError("multiple genesis receipts found")
            genesis = r
        else:
            if prev in by_prev:
                raise ValueError("multiple receipts reference the same previous hash")
            by_prev[prev] = r

    if genesis is None:
        raise ValueError("no genesis receipt found")

    ordered = [genesis]
    seen_hashes = set()

    current = genesis
    while True:
        current_hash = current.get("receipt_hash")

        if current_hash in seen_hashes:
            raise ValueError("cycle detected in receipt chain")

        seen_hashes.add(current_hash)

        nxt = by_prev.get(current_hash)
        if nxt is None:
            break

        ordered.append(nxt)
        current = nxt

    if len(ordered) != len(receipts):
        raise ValueError("disconnected receipts found in chain")

    return ordered


def verify_chain(receipt_dir):
    if not os.path.exists(receipt_dir):
        return {"status": "ok", "reason": "no receipts"}

    receipts = _load_receipts(receipt_dir)

    if not receipts:
        return {"status": "ok", "reason": "empty chain"}

    try:
        ordered = _order_receipts_by_chain(receipts)
    except ValueError as e:
        return {
            "status": "rejected",
            "stage": "chain_integrity",
            "reason": str(e)
        }

    previous_hash = None

    for idx, receipt in enumerate(ordered):
        computed_hash = compute_receipt_hash(receipt)
        if computed_hash != receipt.get("receipt_hash"):
            return {
                "status": "rejected",
                "stage": "receipt_integrity",
                "reason": f"tampered receipt at index {idx}"
            }

        if idx == 0:
            if receipt.get("previous_receipt_hash") is not None:
                return {
                    "status": "rejected",
                    "stage": "chain_integrity",
                    "reason": "genesis receipt must have no previous hash"
                }
        else:
            if receipt.get("previous_receipt_hash") != previous_hash:
                return {
                    "status": "rejected",
                    "stage": "chain_integrity",
                    "reason": f"chain break at index {idx}"
                }

        previous_hash = receipt.get("receipt_hash")

    return {"status": "ok"}


def is_chain_locked(receipt_dir):
    result = verify_chain(receipt_dir)
    return result["status"] != "ok"


def clear_chain_lock(receipt_dir):
    return True

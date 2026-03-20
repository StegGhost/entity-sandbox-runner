import os
import json
import hashlib


def compute_receipt_hash(receipt):
    # exclude receipt_hash itself
    data = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    encoded = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def verify_chain(receipt_dir):
    if not os.path.exists(receipt_dir):
        return {"status": "ok", "reason": "no receipts"}

    files = sorted(os.listdir(receipt_dir))

    previous_hash = None

    for idx, fname in enumerate(files):
        path = os.path.join(receipt_dir, fname)

        with open(path, "r") as f:
            receipt = json.load(f)

        # 🔴 NEW: verify receipt integrity
        computed_hash = compute_receipt_hash(receipt)
        if computed_hash != receipt.get("receipt_hash"):
            return {
                "status": "rejected",
                "stage": "receipt_integrity",
                "reason": f"tampered receipt at index {idx}"
            }

        # 🔴 existing chain linkage check
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
    # no-op for now (kept for interface consistency)
    return True

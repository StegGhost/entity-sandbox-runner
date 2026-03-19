import os
import json
import hashlib
from typing import List, Dict, Any

CHAIN_LOCK_FILE = ".chain_lock"


def _canonical_json(data: Dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def compute_receipt_hash(receipt: Dict[str, Any]) -> str:
    receipt_copy = dict(receipt)
    receipt_copy.pop("receipt_hash", None)
    return hashlib.sha256(_canonical_json(receipt_copy).encode()).hexdigest()


def _load_receipts(receipt_dir: str) -> List[Dict[str, Any]]:
    if not os.path.exists(receipt_dir):
        return []

    files = sorted([
        f for f in os.listdir(receipt_dir)
        if f.endswith(".json")
    ])

    receipts = []
    for f in files:
        path = os.path.join(receipt_dir, f)
        with open(path, "r") as fp:
            receipts.append(json.load(fp))

    return receipts


def verify_chain(receipt_dir: str) -> Dict[str, Any]:
    receipts = _load_receipts(receipt_dir)

    if not receipts:
        return {"valid": True}

    for i, receipt in enumerate(receipts):
        expected_hash = compute_receipt_hash(receipt)

        if receipt.get("receipt_hash") != expected_hash:
            _lock_chain()
            return {
                "valid": False,
                "reason": f"hash mismatch at index {i}"
            }

        if i > 0:
            prev = receipts[i - 1]
            if receipt.get("previous_receipt_hash") != prev.get("receipt_hash"):
                _lock_chain()
                return {
                    "valid": False,
                    "reason": f"chain break at index {i}"
                }

    return {"valid": True}


def _lock_chain():
    with open(CHAIN_LOCK_FILE, "w") as f:
        f.write("CHAIN_COMPROMISED")


def is_chain_locked() -> bool:
    return os.path.exists(CHAIN_LOCK_FILE)


def clear_chain_lock():
    if os.path.exists(CHAIN_LOCK_FILE):
        os.remove(CHAIN_LOCK_FILE)

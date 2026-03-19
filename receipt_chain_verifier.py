import os
import json
import hashlib
from typing import List, Dict, Any


def _load_receipts(receipt_dir: str) -> List[Dict[str, Any]]:
    if not os.path.isdir(receipt_dir):
        return []

    files = sorted(
        [f for f in os.listdir(receipt_dir) if f.endswith(".json")]
    )

    receipts = []
    for f in files:
        path = os.path.join(receipt_dir, f)
        with open(path, "r", encoding="utf-8") as file:
            receipts.append(json.load(file))

    return receipts


def _compute_hash(receipt: Dict[str, Any]) -> str:
    # Remove stored hash before recomputing
    receipt_copy = dict(receipt)
    receipt_copy.pop("receipt_hash", None)

    serialized = json.dumps(receipt_copy, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def verify_chain(receipt_dir: str = "receipts") -> Dict[str, Any]:
    receipts = _load_receipts(receipt_dir)

    if len(receipts) <= 1:
        return {"valid": True}

    for i in range(len(receipts)):
        r = receipts[i]

        # 🔷 Verify content integrity
        expected_hash = r.get("receipt_hash")
        actual_hash = _compute_hash(r)

        if expected_hash != actual_hash:
            return {
                "valid": False,
                "reason": f"receipt tampered at index {i}"
            }

        # 🔷 Verify chain linkage
        if i > 0:
            prev = receipts[i - 1]

            if prev.get("receipt_hash") != r.get("previous_receipt_hash"):
                return {
                    "valid": False,
                    "reason": f"chain break at index {i}"
                }

    return {"valid": True}

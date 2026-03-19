import os
import json
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


def verify_chain(receipt_dir: str = "receipts") -> Dict[str, Any]:
    receipts = _load_receipts(receipt_dir)

    # 🔷 Allow bootstrap states
    if len(receipts) <= 1:
        return {"valid": True}

    for i in range(1, len(receipts)):
        prev = receipts[i - 1]
        curr = receipts[i]

        prev_hash = prev.get("receipt_hash")
        expected_prev = curr.get("previous_receipt_hash")

        if prev_hash != expected_prev:
            return {
                "valid": False,
                "reason": f"chain break at index {i}"
            }

    return {"valid": True}

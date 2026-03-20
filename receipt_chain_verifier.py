import os
import json
import hashlib
from typing import Any, Dict, List, Optional


def compute_hash(data: Any) -> str:
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compute_receipt_hash(receipt):
    payload = {
        k: v
        for k, v in receipt.items()
        if k not in ["receipt_hash", "process_hash"]
    }
    return compute_hash(payload)


def load_receipts(receipt_dir: str) -> List[Dict[str, Any]]:
    if not os.path.exists(receipt_dir):
        return []

    receipts: List[Dict[str, Any]] = []

    for fname in os.listdir(receipt_dir):
        if not fname.endswith(".json"):
            continue

        path = os.path.join(receipt_dir, fname)
        if not os.path.isfile(path):
            continue

        with open(path, "r", encoding="utf-8") as f:
            receipts.append(json.load(f))

    return receipts


def build_chain(receipts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not receipts:
        return []

    by_prev: Dict[Optional[str], List[Dict[str, Any]]] = {}

    for receipt in receipts:
        prev = receipt.get("previous_receipt_hash")
        by_prev.setdefault(prev, []).append(receipt)

    genesis_list = by_prev.get(None, [])
    if len(genesis_list) != 1:
        raise ValueError("chain must contain exactly one genesis receipt")

    ordered: List[Dict[str, Any]] = []
    current = genesis_list[0]
    seen_hashes = set()

    while current is not None:
        current_hash = current.get("receipt_hash")
        if current_hash in seen_hashes:
            raise ValueError("cycle detected in receipt chain")

        seen_hashes.add(current_hash)
        ordered.append(current)

        children = by_prev.get(current_hash, [])
        if len(children) > 1:
            raise ValueError("multiple children found for a receipt hash")

        current = children[0] if children else None

    if len(ordered) != len(receipts):
        raise ValueError("disconnected receipts found in chain")

    return ordered


def verify_chain(receipt_dir: str = "receipts") -> Dict[str, Any]:
    if not os.path.exists(receipt_dir):
        return {"status": "ok", "reason": "no receipts"}

    receipts = load_receipts(receipt_dir)
    if not receipts:
        return {"status": "ok", "reason": "empty chain"}

    try:
        ordered = build_chain(receipts)
    except ValueError as e:
        return {
            "status": "rejected",
            "stage": "chain_integrity",
            "reason": str(e),
        }

    prev_receipt_hash = None
    prev_process_hash = None

    for idx, receipt in enumerate(ordered):
        expected_receipt_hash = compute_receipt_hash(receipt)
        stored_receipt_hash = receipt.get("receipt_hash")

        if expected_receipt_hash != stored_receipt_hash:
            return {
                "status": "rejected",
                "stage": "receipt_integrity",
                "reason": f"tampered receipt at index {idx}",
            }

        if idx == 0:
            if receipt.get("previous_receipt_hash") is not None:
                return {
                    "status": "rejected",
                    "stage": "chain_integrity",
                    "reason": "genesis receipt must have no previous hash",
                }
        else:
            if receipt.get("previous_receipt_hash") != prev_receipt_hash:
                return {
                    "status": "rejected",
                    "stage": "chain_integrity",
                    "reason": f"chain break at index {idx}",
                }

        process_material = {
            "previous_process_hash": prev_process_hash,
            "receipt_hash": stored_receipt_hash,
            "execution_fingerprint": receipt.get("execution_fingerprint"),
        }
        expected_process_hash = compute_hash(process_material)

        if receipt.get("process_hash") != expected_process_hash:
            return {
                "status": "rejected",
                "stage": "process_integrity",
                "reason": f"process hash mismatch at index {idx}",
            }

        prev_receipt_hash = stored_receipt_hash
        prev_process_hash = receipt.get("process_hash")

    return {"status": "ok"}


def is_chain_locked(receipt_dir: str = "receipts") -> bool:
    result = verify_chain(receipt_dir)
    return result.get("status") != "ok"


def clear_chain_lock(receipt_dir: str = "receipts") -> bool:
    # Compatibility no-op. Current architecture uses verification rather than lock files.
    return True

import os
import json
from typing import Any, Dict

from receipt_chain_verifier import verify_chain, load_receipts, build_chain


def reconstruct_state(receipt_dir: str = "receipts", strict: bool = True) -> Dict[str, Any]:
    chain_result = verify_chain(receipt_dir)

    if strict and chain_result.get("status") != "ok":
        raise RuntimeError(f"Chain verification failed: {chain_result}")

    if not os.path.exists(receipt_dir):
        return {}

    receipts = load_receipts(receipt_dir)
    if not receipts:
        return {}

    if strict:
        ordered = build_chain(receipts)
    else:
        try:
            ordered = build_chain(receipts)
        except Exception:
            ordered = []

    state: Dict[str, Any] = {}

    for receipt in ordered:
        result = receipt.get("result", {})
        if isinstance(result, dict):
            state.update(result)

    return state

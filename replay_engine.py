import os
from typing import Dict, Any, List

from receipt_chain_verifier import load_receipts, build_chain
from state_reconstructor import reconstruct_state
from state_hash import compute_state_hash


def replay_chain(receipt_dir: str) -> Dict[str, Any]:
    receipts = load_receipts(receipt_dir)
    ordered = build_chain(receipts)

    states: List[Dict[str, Any]] = []

    current_state: Dict[str, Any] = {}

    for receipt in ordered:
        result = receipt.get("result", {})

        if isinstance(result, dict):
            current_state.update(result)

        states.append({
            "receipt_hash": receipt.get("receipt_hash"),
            "state_hash": compute_state_hash(current_state),
        })

    return {
        "status": "ok",
        "steps": states,
        "final_state": current_state,
        "final_state_hash": compute_state_hash(current_state),
    }

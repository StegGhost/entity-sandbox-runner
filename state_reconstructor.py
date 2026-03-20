import os
from typing import Any, Dict, List

from receipt_chain_verifier import verify_chain, load_receipts, build_chain


def reconstruct_state(receipt_dir: str = "receipts", strict: bool = True) -> Dict[str, Any]:
    chain_result = verify_chain(receipt_dir)

    if strict and not chain_result.get("valid", False):
        raise RuntimeError(f"Chain verification failed: {chain_result}")

    if not os.path.exists(receipt_dir):
        return {
            "materialized_state": {},
            "receipt_count": 0,
            "last_receipt_hash": None,
            "last_process_hash": None,
            "authority_history": [],
            "execution_fingerprints": [],
            "timeline": [],
        }

    receipts = load_receipts(receipt_dir)
    if not receipts:
        return {
            "materialized_state": {},
            "receipt_count": 0,
            "last_receipt_hash": None,
            "last_process_hash": None,
            "authority_history": [],
            "execution_fingerprints": [],
            "timeline": [],
        }

    if strict:
        ordered = build_chain(receipts)
    else:
        try:
            ordered = build_chain(receipts)
        except Exception:
            ordered = []

    materialized_state: Dict[str, Any] = {}
    authority_history: List[Dict[str, Any]] = []
    execution_fingerprints: List[str] = []
    timeline: List[Dict[str, Any]] = []

    last_receipt_hash = None
    last_process_hash = None

    for idx, receipt in enumerate(ordered):
        result = receipt.get("result", {})
        if isinstance(result, dict):
            materialized_state.update(result)

        authority = receipt.get("authority", {})
        authority_history.append({
            "index": idx,
            "authority_id": authority.get("authority_id"),
            "authority": authority,
        })

        execution_fingerprint = receipt.get("execution_fingerprint")
        if execution_fingerprint is not None:
            execution_fingerprints.append(execution_fingerprint)

        timeline.append({
            "index": idx,
            "proposal": receipt.get("proposal"),
            "timestamp": receipt.get("timestamp"),
            "receipt_hash": receipt.get("receipt_hash"),
            "process_hash": receipt.get("process_hash"),
            "state_before_hash": receipt.get("state_before_hash"),
            "state_after_hash": receipt.get("state_after_hash"),
        })

        last_receipt_hash = receipt.get("receipt_hash")
        last_process_hash = receipt.get("process_hash")

    return {
        "materialized_state": materialized_state,
        "receipt_count": len(ordered),
        "last_receipt_hash": last_receipt_hash,
        "last_process_hash": last_process_hash,
        "authority_history": authority_history,
        "execution_fingerprints": execution_fingerprints,
        "timeline": timeline,
    }

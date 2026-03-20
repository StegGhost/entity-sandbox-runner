import json
import os
import time
import hashlib
import uuid
from typing import Any, Dict, Optional


def _hash(data: Any) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode("utf-8")
    ).hexdigest()


def _compute_execution_fingerprint(
    proposal: Dict[str, Any],
    result: Any,
    decision: Dict[str, Any],
    authority: Dict[str, Any],
) -> str:
    payload = {
        "proposal": proposal,
        "result": result,
        "decision": decision,
        "authority": authority,
    }
    return _hash(payload)


def record_decision(
    proposal: Dict[str, Any],
    result: Any,
    u_value: float,
    decision: Dict[str, Any],
    authority: Dict[str, Any],
    previous_receipt_hash: Optional[str],
    receipt_dir: str,
    previous_process_hash: Optional[str] = None,
) -> Dict[str, Any]:
    os.makedirs(receipt_dir, exist_ok=True)

    execution_fingerprint = _compute_execution_fingerprint(
        proposal=proposal,
        result=result,
        decision=decision,
        authority=authority,
    )

    receipt: Dict[str, Any] = {
        "schema_version": "4.0.0",
        "timestamp": time.time(),
        "proposal": proposal.get("name"),
        "result": result,
        "u_value": u_value,
        "decision": decision,
        "authority": authority,
        "previous_receipt_hash": previous_receipt_hash,
        "execution_fingerprint": execution_fingerprint,
    }

    # First-layer integrity hash
    receipt["receipt_hash"] = _hash({
        k: v for k, v in receipt.items()
        if k not in ["receipt_hash", "process_hash", "receipt_path"]
    })

    # Second-layer process lineage hash
    process_material = {
        "previous_process_hash": previous_process_hash,
        "receipt_hash": receipt["receipt_hash"],
        "execution_fingerprint": execution_fingerprint,
    }
    receipt["process_hash"] = _hash(process_material)

    filename = (
        f"{time.time_ns()}_"
        f"{receipt['receipt_hash'][:10]}_"
        f"{uuid.uuid4().hex[:6]}.json"
    )
    path = os.path.join(receipt_dir, filename)
    tmp_path = path + ".tmp"

    # Atomic write
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)

    os.replace(tmp_path, path)

    receipt["receipt_path"] = path
    return receipt

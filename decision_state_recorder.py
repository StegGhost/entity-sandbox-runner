import os
import json
import time
import hashlib
from typing import Dict, Any, Optional


def _hash(data: Dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(data, sort_keys=True, default=str).encode()
    ).hexdigest()


def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def record_decision(
    proposal: Dict[str, Any],
    result: Dict[str, Any],
    u_value: float,
    decision: Dict[str, Any],
    authority: Dict[str, Any],
    previous_receipt_hash: Optional[str] = None,
    receipt_dir: str = "receipts",
) -> Dict[str, Any]:

    timestamp = time.time()

    state_snapshot = {
        "proposal": proposal.get("name"),
        "u": u_value,
        "decision": decision.get("action"),
    }

    receipt = {
        "schema_version": "2.0.0",
        "timestamp": timestamp,
        "proposal": proposal.get("name"),
        "result": result,
        "u_value": u_value,
        "decision": decision,
        "authority": authority,
        "state_snapshot_hash": _hash(state_snapshot),
        "previous_receipt_hash": previous_receipt_hash,
    }

    receipt["receipt_hash"] = _hash(receipt)

    _ensure_dir(receipt_dir)

    filename = f"{int(timestamp)}_{receipt['receipt_hash'][:12]}.json"
    path = os.path.join(receipt_dir, filename)

    with open(path, "w") as f:
        json.dump(receipt, f, indent=2)

    receipt["receipt_path"] = path

    return receipt

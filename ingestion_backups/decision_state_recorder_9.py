import os
import json
import time
import hashlib
from typing import Dict, Any


def _compute_hash(receipt: Dict[str, Any]) -> str:
    # Remove hash before computing
    r = dict(receipt)
    r.pop("receipt_hash", None)

    serialized = json.dumps(r, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def record_decision(
    proposal: Dict[str, Any],
    result: Dict[str, Any],
    u_value: float,
    decision: Dict[str, Any],
    authority: Dict[str, Any],
    previous_receipt_hash: str,
    receipt_dir: str = "receipts",
) -> Dict[str, Any]:

    os.makedirs(receipt_dir, exist_ok=True)

    timestamp = time.time()

    receipt = {
        "schema_version": "2.0.0",
        "timestamp": timestamp,
        "proposal": proposal.get("name"),
        "result": result,
        "u_value": u_value,
        "decision": decision,
        "authority": authority,
        "previous_receipt_hash": previous_receipt_hash,
    }

    # 🔷 Compute hash AFTER full structure is set
    receipt_hash = _compute_hash(receipt)
    receipt["receipt_hash"] = receipt_hash

    filename = f"{int(timestamp)}_{receipt_hash[:10]}.json"
    path = os.path.join(receipt_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, sort_keys=True)

    receipt["receipt_path"] = path

    return receipt

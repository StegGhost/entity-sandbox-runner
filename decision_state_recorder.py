import time
from typing import Any, Dict

from receipt_chain_verifier import compute_hash
from state_hash import compute_state_hash


def build_decision_record(
    proposal: Dict[str, Any],
    authority: Dict[str, Any],
    decision: Dict[str, Any],
    state_snapshot: Dict[str, Any],
    u_value: float,
) -> Dict[str, Any]:
    record = {
        "schema_version": "1.0.0",
        "timestamp": time.time(),
        "proposal": proposal.get("name"),
        "authority": authority,
        "decision": decision,
        "u_value": u_value,
        "state_hash": compute_state_hash(state_snapshot),
    }

    record["decision_hash"] = compute_hash(record)
    return record

from typing import Dict, Any

from state_hash import compute_state_hash


def verify_decision_record(
    decision_record: Dict[str, Any],
    reconstructed_state: Dict[str, Any],
) -> Dict[str, Any]:

    expected_state_hash = decision_record.get("state_hash")
    actual_state_hash = compute_state_hash(reconstructed_state)

    if expected_state_hash != actual_state_hash:
        return {
            "valid": False,
            "reason": "state_mismatch",
            "expected": expected_state_hash,
            "actual": actual_state_hash,
        }

    if not decision_record.get("decision", {}).get("allowed", False):
        return {
            "valid": False,
            "reason": "decision_not_allowed",
        }

    return {
        "valid": True,
    }

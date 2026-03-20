from typing import Dict, Any, List


def check_invariants(receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    violations = []

    for i, receipt in enumerate(receipts):
        decision = receipt.get("decision", {})
        result = receipt.get("result", {})
        decision_record = receipt.get("decision_record")

        # Invariant 1: committed must have allowed decision
        if decision.get("allowed") is not True:
            violations.append({
                "index": i,
                "type": "invalid_commit",
                "reason": "decision_not_allowed",
            })

        # Invariant 2: decision_record must exist
        if not decision_record:
            violations.append({
                "index": i,
                "type": "missing_decision_record",
            })

        # Invariant 3: decision_hash must match
        if decision_record:
            if receipt.get("decision_hash") != decision_record.get("decision_hash"):
                violations.append({
                    "index": i,
                    "type": "decision_hash_mismatch",
                })

    return {
        "valid": len(violations) == 0,
        "violations": violations,
    }

from typing import Dict, Any, List


def check_invariants(receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    violations = []

    for i, receipt in enumerate(receipts):
        schema_version = str(receipt.get("schema_version", "0.0.0"))
        decision = receipt.get("decision", {})
        decision_record = receipt.get("decision_record")

        # Only enforce new decision-record invariants on governed receipts
        if schema_version < "4.2.0":
            continue

        # Only committed / allowed decisions must satisfy invariants
        if decision.get("allowed", False) is not True:
            continue

        # Invariant 1: governed committed receipts must have decision_record
        if not decision_record:
            violations.append({
                "index": i,
                "type": "missing_decision_record",
            })
            continue

        # Invariant 2: decision_hash must match embedded decision_record
        if receipt.get("decision_hash") != decision_record.get("decision_hash"):
            violations.append({
                "index": i,
                "type": "decision_hash_mismatch",
            })

    return {
        "valid": len(violations) == 0,
        "violations": violations,
    }

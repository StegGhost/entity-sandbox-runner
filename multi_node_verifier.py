from typing import Any, Dict, List

from receipt_chain_verifier import verify_chain
from state_reconstructor import reconstruct_state
from state_hash import compute_state_hash
from weighted_consensus import weighted_consensus


def verify_nodes(node_dirs: List[str]) -> Dict[str, Any]:
    results = []

    for node_dir in node_dirs:
        chain_result = verify_chain(node_dir)

        if not chain_result.get("valid", False):
            results.append({
                "node": node_dir,
                "valid": False,
                "reason": chain_result.get("reason"),
                "state_hash": None,
                "state": None,
                "trust_score": 0.1,
                "energy_cost": 2.0,
                "compute_cost": 2.0,
            })
            continue

        try:
            state = reconstruct_state(node_dir, strict=True)
            state_hash = compute_state_hash(state)

            results.append({
                "node": node_dir,
                "valid": True,
                "reason": None,
                "state_hash": state_hash,
                "state": state,
                "trust_score": 1.0,
                "energy_cost": 0.8,
                "compute_cost": 1.0,
            })

        except Exception as e:
            results.append({
                "node": node_dir,
                "valid": False,
                "reason": str(e),
                "state_hash": None,
                "state": None,
                "trust_score": 0.2,
                "energy_cost": 2.0,
                "compute_cost": 2.0,
            })

    any_invalid = any(not r["valid"] for r in results)

    consensus_result = weighted_consensus(results)

    final_consensus = (
        consensus_result.get("consensus", False) and not any_invalid
    )

    return {
        "consensus": final_consensus,
        "consensus_hash": consensus_result.get("state_hash"),
        "confidence": consensus_result.get("confidence"),
        "results": results,
    }


def verify_multi_node_state(
    receipt_dir_a: str = "receipts_node_a",
    receipt_dir_b: str = "receipts_node_b",
) -> Dict[str, Any]:
    return verify_nodes([receipt_dir_a, receipt_dir_b])

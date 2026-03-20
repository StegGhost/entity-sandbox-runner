from typing import Any, Dict, List

from receipt_chain_verifier import verify_chain
from state_reconstructor import reconstruct_state
from state_hash import compute_state_hash


def verify_nodes(node_dirs: List[str]) -> Dict[str, Any]:
    results = []

    for node_dir in node_dirs:
        chain_result = verify_chain(node_dir)

        if chain_result.get("status") != "ok":
            results.append({
                "node": node_dir,
                "valid": False,
                "reason": chain_result.get("reason"),
                "state_hash": None,
                "state": None,
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
            })
        except Exception as e:
            results.append({
                "node": node_dir,
                "valid": False,
                "reason": str(e),
                "state_hash": None,
                "state": None,
            })

    valid_results = [r for r in results if r["valid"]]

    if len(valid_results) < 2:
        return {
            "consensus": False,
            "results": results,
        }

    consensus = len({r["state_hash"] for r in valid_results}) == 1

    return {
        "consensus": consensus,
        "results": results,
    }


def verify_multi_node_state(
    receipt_dir_a: str = "receipts_node_a",
    receipt_dir_b: str = "receipts_node_b",
) -> Dict[str, Any]:
    return verify_nodes([receipt_dir_a, receipt_dir_b])

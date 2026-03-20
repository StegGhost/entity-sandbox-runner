from typing import Any, Dict, List

from state_reconstructor import reconstruct_state
from state_hash import compute_state_hash


def verify_nodes(node_dirs: List[str]) -> Dict[str, Any]:
    results = []

    for node_dir in node_dirs:
        state = reconstruct_state(node_dir, strict=True)
        state_hash = compute_state_hash(state)

        results.append({
            "node": node_dir,
            "state_hash": state_hash,
            "state": state,
        })

    consensus = len({r["state_hash"] for r in results}) == 1

    return {
        "consensus": consensus,
        "results": results,
    }


def verify_multi_node_state(receipt_dir_a: str = "receipts_node_a", receipt_dir_b: str = "receipts_node_b") -> Dict[str, Any]:
    return verify_nodes([receipt_dir_a, receipt_dir_b])

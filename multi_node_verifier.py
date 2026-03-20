from state_reconstructor import reconstruct_state
from state_hash import compute_state_hash


def verify_nodes(node_dirs):
    results = []

    for node_dir in node_dirs:
        state = reconstruct_state(node_dir, strict=False)
        state_hash = compute_state_hash(state)

        results.append({
            "node": node_dir,
            "state_hash": state_hash,
            "state": state
        })

    hashes = [r["state_hash"] for r in results]

    return {
        "consensus": len(set(hashes)) == 1,
        "results": results
    }

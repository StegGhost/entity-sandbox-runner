from state_reconstructor import reconstruct_state
from state_hash import compute_state_hash


def verify_nodes(node_dirs):
    results = []

    for node_dir in node_dirs:
        state = reconstruct_state(node_dir, strict=False)  # 🔥 key change
        state_hash = compute_state_hash(state)

        results.append({
            "node": node_dir,
            "state": state,
            "hash": state_hash
        })

    hashes = [r["hash"] for r in results]
    consensus = len(set(hashes)) == 1

    return {
        "consensus": consensus,
        "results": results
    }

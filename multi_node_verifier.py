import os
import json
from receipt_chain_verifier import verify_chain
from state_reconstructor import reconstruct_state


def verify_nodes_weighted(nodes):
    results = []
    total_weight = 0
    agreement_weight = {}

    for node in nodes:
        result = verify_chain(node["path"])

        if result["status"] != "ok":
            continue

        state = reconstruct_state(node["path"], strict=True)
        state_hash = json.dumps(state, sort_keys=True)

        weight = node.get("trust_score", 1.0)

        total_weight += weight

        agreement_weight[state_hash] = agreement_weight.get(state_hash, 0) + weight

        results.append({
            "node": node["name"],
            "state_hash": state_hash,
            "weight": weight,
            "state": state
        })

    if not agreement_weight:
        return {"consensus": False, "results": results}

    best_state = max(agreement_weight, key=agreement_weight.get)
    best_weight = agreement_weight[best_state]

    consensus = best_weight / total_weight >= 0.67

    return {
        "consensus": consensus,
        "confidence": best_weight / total_weight,
        "results": results
    }

from typing import List, Dict


def weighted_consensus(results: List[Dict]) -> Dict:
    valid_nodes = [r for r in results if r.get("valid")]

    if not valid_nodes:
        return {"consensus": False, "reason": "no valid nodes"}

    buckets = {}

    for node in valid_nodes:
        h = node["state_hash"]
        weight = node.get("trust_score", 1.0)

        if h not in buckets:
            buckets[h] = 0.0

        buckets[h] += weight

    best_hash = max(buckets, key=buckets.get)
    total_weight = sum(buckets.values())

    confidence = buckets[best_hash] / total_weight if total_weight else 0

    return {
        "consensus": confidence > 0.5,
        "state_hash": best_hash,
        "confidence": confidence,
        "weights": buckets,
    }

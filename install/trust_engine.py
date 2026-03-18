
def update_trust_scores(state, peer_receipts):
    scores = state.get("peer_trust", {})
    for r in peer_receipts:
        peer = r.get("source", "unknown")
        u = r.get("u", 0.5)

        if peer not in scores:
            scores[peer] = {"score": 0.5, "count": 0}

        scores[peer]["score"] = (scores[peer]["score"] + u) / 2
        scores[peer]["count"] += 1

    state["peer_trust"] = scores
    return scores

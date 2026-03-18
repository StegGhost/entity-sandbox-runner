
def weighted_consensus(local_action, peer_receipts):
    score = {
        "allow": 0.0,
        "monitor": 0.0,
        "restrict": 0.0
    }

    score[local_action] += 1.0

    for r in peer_receipts:
        action = r.get("consensus_action") or r.get("action")
        u = r.get("u", 0.5)
        weight = max(0.1, min(1.0, u))

        if action in score:
            score[action] += weight

    return max(score, key=score.get)


def filter_adversarial(peers, trust_scores, threshold=0.3):
    clean = []
    for r in peers:
        peer = r.get("source", "unknown")
        trust = trust_scores.get(peer, {}).get("score", 0.5)
        if trust >= threshold:
            clean.append(r)
    return clean

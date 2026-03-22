
def consensus_score(scores):
    return min(scores)

def is_network_stable(scores, threshold=1.0):
    return consensus_score(scores) >= threshold

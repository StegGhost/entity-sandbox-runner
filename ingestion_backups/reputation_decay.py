
def decay(scores, factor=0.95):
    for k in scores:
        scores[k]["score"] *= factor
    return scores

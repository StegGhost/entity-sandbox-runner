def quorum(results, threshold=0.6):
    counts = {}
    for r in results:
        counts[r] = counts.get(r, 0) + 1
    total = len(results)
    best = max(counts, key=counts.get)
    if counts[best] / total >= threshold:
        return {"decision": best, "confidence": counts[best] / total}
    return {"decision": None, "confidence": 0}

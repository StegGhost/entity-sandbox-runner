def estimate_probability(results):
    if not results:
        return 0.0
    collapse_count = 0
    for r in results:
        metrics = r.get("metrics", {}) if isinstance(r, dict) else {}
        if metrics.get("collapse", False):
            collapse_count += 1
    return collapse_count / len(results)

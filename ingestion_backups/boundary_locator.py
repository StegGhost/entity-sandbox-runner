def locate_boundary(data):
    ordered = sorted(data, key=lambda x: x["ratio"])
    lower = upper = None
    for i in range(1, len(ordered)):
        prev = ordered[i - 1]
        curr = ordered[i]
        if (not prev["collapse"]) and curr["collapse"]:
            lower = prev["ratio"]
            upper = curr["ratio"]
            break
    return {"lower": lower, "upper": upper, "found": lower is not None and upper is not None}

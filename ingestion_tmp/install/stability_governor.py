
def classify(u):
    if u > 0.75:
        return "stable", "allow"
    elif u > 0.6:
        return "warning", "monitor"
    return "critical", "restrict"

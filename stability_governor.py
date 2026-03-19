def evaluate_stability(u_value):
    """
    Determines system stability class and action based on U
    """

    if u_value > 0.85:
        return {
            "action": "allow",
            "class": "stable",
            "threshold": 0.85
        }

    elif u_value > 0.65:
        return {
            "action": "allow",
            "class": "elastic",
            "threshold": 0.65
        }

    elif u_value > 0.45:
        return {
            "action": "allow",
            "class": "degrading",
            "threshold": 0.45
        }

    else:
        return {
            "action": "reject",
            "class": "unstable",
            "threshold": 0.45,
            "reason": "u_below_minimum_threshold"
        }

import math

def compute_u(components, weights=None):
    """
    components = {
        "stability": float,
        "trust": float,
        "constraint_pressure": float,
        "history": float
    }
    """

    if weights is None:
        weights = {
            "stability": 0.25,
            "trust": 0.25,
            "constraint_pressure": 0.25,
            "history": 0.25
        }

    s = components.get("stability", 0)
    t = components.get("trust", 0)
    k = components.get("constraint_pressure", 0)
    h = components.get("history", 1)

    # invert constraint pressure
    k_term = 1 - k

    U = (
        weights["stability"] * s +
        weights["trust"] * t +
        weights["constraint_pressure"] * k_term +
        weights["history"] * h
    )

    return max(0.0, min(1.0, U))

def refine_grid(lower, upper, points=10, population=200, steps=500):
    if lower is None or upper is None:
        return []
    width = upper - lower
    step = width / max(points - 1, 1)
    grid = []
    x = lower
    while x <= upper + 1e-12:
        grid.append({"population": population, "adversarial_ratio": round(x, 6), "steps": steps})
        x += step
    return grid

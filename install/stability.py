
def compute_stability(history):
    if len(history) < 2:
        return 1.0

    diffs = [abs(history[i] - history[i-1]) for i in range(1, len(history))]
    return 1.0 - (sum(diffs) / len(diffs))

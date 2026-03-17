def weighted_score(state):
    history = state.get("history", [])[-20:]
    if not history:
        return 0.5
    # Weight recent confidence by decision success
    total = 0.0
    denom = 0.0
    for i, item in enumerate(history, start=1):
        recency = i / len(history)
        decision_weight = 1.0 if item.get("decision") == "ok" else 0.55
        total += item.get("confidence", 0.5) * recency * decision_weight
        denom += recency
    return round(total / max(denom, 1e-9), 6)

def weighted_mode(state, u_signal, action):
    if action == "restrict" or u_signal < 0.60:
        return "conservative"
    if u_signal > 0.84:
        return "aggressive"
    return "normal"

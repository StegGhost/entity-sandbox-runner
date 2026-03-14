def apply_trust_drift(state, rate):

    state["t"] -= rate

    if state["t"] < 0:
        state["t"] = 0

    return state

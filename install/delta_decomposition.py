def decompose_delta(prev_state, current_state):
    det = {}
    unc = {}

    for k in current_state:
        if prev_state.get(k) == current_state[k]:
            det[k] = current_state[k]
        else:
            try:
                diff = abs(current_state[k] - prev_state.get(k, 0))
                if diff < 1e-6:
                    det[k] = current_state[k]
                else:
                    unc[k] = current_state[k]
            except:
                unc[k] = current_state[k]

    return det, unc


def uncertainty_norm(unc):
    return sum(abs(v) for v in unc.values()) if unc else 0.0

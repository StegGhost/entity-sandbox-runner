from install.delta_decomposition import decompose_delta, uncertainty_norm

def enforce_delta_guard(prev_state, current_state, epsilon=0.25):
    det, unc = decompose_delta(prev_state, current_state)
    norm = uncertainty_norm(unc)

    if norm > epsilon:
        return False, norm, det, unc

    return True, norm, det, unc

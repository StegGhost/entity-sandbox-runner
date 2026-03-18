def apply_finco(u, external_signal=None):
    if external_signal is None:
        return u
    return max(0.0, min(1.0, (u + external_signal) / 2))

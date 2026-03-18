
def escalation_layer(u, stability):
    if stability < 0.4:
        return "restrict", "instability_detected"
    if u < 0.4:
        return "restrict", "low_signal"
    return None, None

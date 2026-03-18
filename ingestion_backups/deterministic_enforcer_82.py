def enforce_policy(state, proposed_action, proposed_state, u_signal):
    failures = len(state.get("failures", []))
    anomalies = len(state.get("anomalies", []))
    mode = state.get("mode", "normal")

    # Hard boundary 1: severe instability
    if u_signal < 0.50:
        return "restrict", "hard_boundary_low_u"

    # Hard boundary 2: too many failures
    if failures >= 12:
        return "restrict", "failure_threshold"

    # Hard boundary 3: anomaly burst
    if anomalies >= 5 and proposed_action == "allow":
        return "monitor", "anomaly_burst"

    # Boundary-conditioned downgrade
    if mode == "conservative" and proposed_action == "allow":
        return "monitor", "conservative_mode_downgrade"

    return proposed_action, "as_proposed"

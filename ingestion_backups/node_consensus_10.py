def compute_node_decision(action, u_signal):
    if u_signal < 0.5:
        return "node_restrict"
    if action == "allow":
        return "node_allow"
    if action == "restrict":
        return "node_restrict"
    return "node_monitor"

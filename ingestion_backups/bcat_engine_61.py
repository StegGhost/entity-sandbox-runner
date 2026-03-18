def enforce_bcat(policy, u):
    hard_stop = policy.get("hard_stop_u", 0.5)
    hard_min = policy.get("hard_min_u", hard_stop)
    soft_min = policy.get("soft_min_u", hard_min)

    if u < hard_stop:
        return "halt", "below_hard_stop"

    if u < hard_min:
        return "restrict", "below_hard_min"

    if u < soft_min:
        return "monitor", "below_soft_min"

    return "allow", "within_bounds"

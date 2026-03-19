def decide(U, policy):
    if U < policy.get("hard_stop_u", 0.3):
        return "halt", "U below hard stop"

    if U < policy.get("restrict_u", 0.6):
        return "restrict", "U below restrict threshold"

    return "allow", "U within safe bounds"

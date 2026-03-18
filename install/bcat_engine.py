def enforce_bcat(policy, u):
    if u < policy["hard_stop_u"]:
        raise Exception("BCAT HARD STOP")

    if u < policy["restrict_u"]:
        return "restrict","boundary_enforced"

    if u > policy["allow_u"]:
        return "allow","boundary_enforced"

    return "monitor","mid_band"

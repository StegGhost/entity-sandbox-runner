def enforce_policy(state, proposed_action, proposed_state, u_signal):
    if u_signal < 0.50: return 'restrict','hard_boundary_low_u'
    if len(state.get('failures',[]))>=15: return 'restrict','failure_ceiling'
    if proposed_action=='allow' and state.get('mode')=='conservative': return 'monitor','mode_override'
    return proposed_action,'as_proposed'

import time

def classify_action(action):
    if "DELETE" in action.upper():
        return "dangerous"
    if "SEND" in action.upper():
        return "moderate"
    return "safe"

def admit_action(passport, action, system_state):
    capabilities = passport.get("capabilities", [])
    required_map = {
        "SEND_EMAIL": "COMM.EMAIL_SEND",
        "READ_EMAIL": "COMM.EMAIL_READ",
        "SCHEDULE_EVENT": "SCHED.CALENDAR"
    }

    required = required_map.get(action)
    classification = classify_action(action)

    if not required:
        return {"allowed": False, "reason": "no_mapping", "classification": classification}

    if required not in capabilities:
        return {"allowed": False, "reason": "missing_capability", "classification": classification}

    return {
        "allowed": True,
        "reason": "authorized",
        "classification": classification,
        "timestamp": time.time(),
        "state_hash": system_state.get("hash")
    }

# stability_governor.py

def decide(state):
    if state == "healthy":
        return "run"
    if state == "caution":
        return "throttle"
    if state == "critical":
        return "restrict"
    return "halt"

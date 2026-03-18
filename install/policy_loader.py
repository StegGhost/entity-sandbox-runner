import json, os

POLICY_PATH = "config/policy.json"

def load_policy():
    if os.path.exists(POLICY_PATH):
        return json.load(open(POLICY_PATH))
    return {
        "thresholds": {
            "allow": 0.65,
            "restrict": 0.55
        },
        "mode": "balanced"
    }

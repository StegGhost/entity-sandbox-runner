import hashlib
import json

REMOTE_POLICY_SHARED_SECRET = "stegverse-remote-policy-secret"

def verify_remote_policy_signature(policy):
    if not isinstance(policy, dict):
        return False

    signature = policy.get("signature")
    if not isinstance(signature, str):
        return False

    material = {
        "hard_stop_u": policy.get("hard_stop_u"),
        "restrict_u": policy.get("restrict_u"),
        "allow_u": policy.get("allow_u"),
    }
    raw = json.dumps(material, sort_keys=True) + REMOTE_POLICY_SHARED_SECRET
    expected = hashlib.sha256(raw.encode()).hexdigest()
    return signature == expected

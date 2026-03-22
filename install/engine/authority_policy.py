
from engine.key_registry import load_registry

# Define path-level authority requirements
PATH_POLICIES = {
    "install/tests/": {"min_role": "sdk_user"},
    "install/engine/": {"min_role": "admin"},
    ".github/workflows/": {"min_role": "admin"},
    "ingestion/": {"min_role": "admin"},
}

ROLE_ORDER = {
    "sdk_user": 1,
    "admin": 2,
}

def get_role_for_key(key_id):
    reg = load_registry()
    entry = reg.get(key_id)
    if not entry:
        return None
    return entry.get("issuer_type")

def is_authorized(path: str, key_id: str):
    role = get_role_for_key(key_id)
    if not role:
        return False, "unknown_key"

    required_role = "sdk_user"

    for prefix, policy in PATH_POLICIES.items():
        if path.startswith(prefix):
            required_role = policy["min_role"]
            break

    if ROLE_ORDER.get(role, 0) < ROLE_ORDER.get(required_role, 0):
        return False, f"insufficient_role:{role}<{required_role}"

    return True, "ok"

def validate_paths(manifest: dict):
    sig = manifest.get("signature", {})
    key_id = sig.get("key_id")

    if not key_id:
        return {"valid": False, "reason": "missing_key_id"}

    violations = []

    for f in manifest.get("files", []):
        path = f.get("path", "")
        ok, reason = is_authorized(path, key_id)
        if not ok:
            violations.append(f"{path}:{reason}")

    if violations:
        return {
            "valid": False,
            "reason": "authority_violation",
            "violations": violations
        }

    return {"valid": True}

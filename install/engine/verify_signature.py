
def verify_signature(manifest):
    sig = manifest.get("signature")
    if not sig:
        return {"valid": False, "reason": "missing_signature"}

    if "key_id" not in sig:
        return {"valid": False, "reason": "missing_key_id"}

    return {"valid": True, "reason": "stub_pass"}

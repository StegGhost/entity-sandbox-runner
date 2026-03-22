
from engine.key_registry import get_public_key
from engine.ed25519_utils import verify_manifest

def verify_multi_signature(manifest):
    sigs = manifest.get("signatures", [])

    if not sigs:
        return {"valid": False, "reason": "missing_signatures"}

    valid_count = 0

    for sig in sigs:
        key_id = sig.get("key_id")
        pk = get_public_key(key_id)
        if not pk:
            continue

        temp_manifest = dict(manifest)
        temp_manifest["signature"] = sig

        res = verify_manifest(temp_manifest, pk)
        if res.get("valid"):
            valid_count += 1

    if valid_count < 2:
        return {"valid": False, "reason": "insufficient_signatures"}

    return {"valid": True}


from engine.multi_sig_policy import requires_multi_sig
from engine.multi_sig_verify import verify_multi_signature

def enforce_multi_sig(manifest):
    files = manifest.get("files", [])

    for f in files:
        path = f.get("path", "")
        if requires_multi_sig(path):
            result = verify_multi_signature(manifest)
            if not result.get("valid"):
                return {"valid": False, "reason": result.get("reason")}
            return {"valid": True}

    return {"valid": True}

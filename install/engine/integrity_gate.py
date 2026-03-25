
from engine.verify_bundle_integrity import verify_integrity
from engine.verify_signature import verify_signature

def run_integrity_gate(extracted_root, manifest):
    sig = verify_signature(manifest)
    if not sig["valid"]:
        return {"valid": False, "reason": f"signature:{sig['reason']}"}

    integrity = verify_integrity(extracted_root, manifest)
    if not integrity["valid"]:
        return {"valid": False, "reason": f"integrity:{integrity['file_errors']}"}

    return {"valid": True}

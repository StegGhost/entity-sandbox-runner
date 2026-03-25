
from engine.governance_pipeline import run_governance_pipeline
from engine.governance_multi_sig_extension import enforce_multi_sig
from engine.key_lifecycle import is_revoked
from engine.governance_receipt import record_receipt
from engine.distributed_validation import validate_across_nodes

def run_full_governance(extracted_root, manifest):
    key_id = manifest.get("signature", {}).get("key_id")
    if key_id and is_revoked(key_id):
        record_receipt(manifest, "rejected", "revoked_key")
        return {"valid": False, "reason": "revoked_key"}

    base = run_governance_pipeline(extracted_root, manifest)
    if not base.get("valid"):
        record_receipt(manifest, "rejected", base.get("stage"))
        return base

    ms = enforce_multi_sig(manifest)
    if not ms.get("valid"):
        record_receipt(manifest, "rejected", "multi_sig")
        return ms

    dist = validate_across_nodes(base)
    record_receipt(manifest, "accepted", "final")

    return dist

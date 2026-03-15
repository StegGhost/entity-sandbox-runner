def verify_contract(manifest, evidence):
    if not manifest:
        return {"verified": False, "reason": "missing_manifest"}
    if "bundle_name" not in manifest:
        return {"verified": False, "reason": "invalid_manifest"}
    return {"verified": True, "reason": "contract_verified"}
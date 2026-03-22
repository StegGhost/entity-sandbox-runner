import json
import hashlib

def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def hash_data(data):
    return hashlib.sha256(canonical_json(data).encode()).hexdigest()

def sign_receipt(receipt, private_key="stub_private_key"):
    # placeholder signing (replace with Ed25519 later)
    core_hash = hash_data(receipt)
    signature = hashlib.sha256((core_hash + private_key).encode()).hexdigest()
    return signature

def verify_receipt_signature(receipt, signature, public_key="stub_public_key"):
    # placeholder verification
    expected = hashlib.sha256((hash_data(receipt) + "stub_private_key").encode()).hexdigest()
    return signature == expected

def create_signed_receipt(receipt):
    signature = sign_receipt(receipt)
    receipt["signature"] = signature
    return receipt

def verify_signed_receipt(receipt):
    sig = receipt.get("signature")
    if not sig:
        return False, "missing_signature"
    core = receipt.copy()
    core.pop("signature")
    valid = verify_receipt_signature(core, sig)
    return valid, "valid" if valid else "invalid_signature"

import hmac
import hashlib

# In production → replace with real key store / public keys
SECRET_KEYS = {
    "admin": b"supersecretkey",
    "agent_alpha": b"alpha_key"
}

def verify_signature(proposal: dict) -> bool:
    authority = proposal.get("authority_id")
    signature = proposal.get("signature")

    if authority not in SECRET_KEYS or not signature:
        return False

    payload = str(proposal.get("payload", "")).encode()

    expected = hmac.new(
        SECRET_KEYS[authority],
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

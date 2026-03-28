import json
import hashlib
from pathlib import Path
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

KEY_DIR = Path(__file__).parent / "keys"


def load_private(name):
    path = KEY_DIR / f"{name}.sk"
    return SigningKey(path.read_text().strip(), encoder=HexEncoder)


def load_public(name):
    path = KEY_DIR / f"{name}.pk"
    return VerifyKey(path.read_text().strip(), encoder=HexEncoder)


def sign_payload(name, payload):
    sk = load_private(name)
    raw = json.dumps(payload, sort_keys=True).encode()
    sig = sk.sign(raw).signature.hex()

    return {
        "signer": name,
        "signature": sig
    }


def verify_signature(name, payload, signature):
    vk = load_public(name)
    raw = json.dumps(payload, sort_keys=True).encode()

    try:
        vk.verify(raw, bytes.fromhex(signature))
        return True
    except Exception:
        return False

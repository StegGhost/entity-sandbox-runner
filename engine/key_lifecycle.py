
from pathlib import Path
import json

REG = Path("config/key_registry.json")
REVOKED = Path("config/revoked_keys.json")

def load(p):
    if not p.exists(): return {}
    return json.loads(p.read_text())

def save(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2))

def revoke_key(key_id):
    data = load(REVOKED)
    data[key_id] = {"revoked": True}
    save(REVOKED, data)

def is_revoked(key_id):
    return load(REVOKED).get(key_id, {}).get("revoked", False)

def rotate_key(old_key, new_key, new_pub, issuer):
    reg = load(REG)
    reg[new_key] = {"public_key": new_pub, "issuer_type": issuer}
    if old_key in reg:
        revoke_key(old_key)
    save(REG, reg)

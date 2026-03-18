
import hashlib, json
SECRET="stegverse-key"

def hash_payload(p):
    return hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest()

def sign_payload(p):
    raw=json.dumps(p,sort_keys=True)+SECRET
    return hashlib.sha256(raw.encode()).hexdigest()

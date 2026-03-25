
import hashlib
def anchor_state(data):
    return hashlib.sha256(str(data).encode()).hexdigest()

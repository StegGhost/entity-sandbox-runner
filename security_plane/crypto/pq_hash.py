import hashlib

def hash_bytes(data: bytes):
    h = hashlib.sha3_256()
    h.update(data)
    return h.hexdigest()

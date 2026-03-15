import hashlib

def pq_hash(data: bytes):
    return hashlib.sha3_512(data).hexdigest()
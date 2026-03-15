from .pq_hash import hash_bytes

def hash_file(path):
    with open(path, "rb") as f:
        data = f.read()
    return hash_bytes(data)

import hashlib, time

chain = []

def record(event):
    prev = chain[-1]["hash"] if chain else "genesis"
    payload = f"{prev}{event}{time.time()}".encode()
    h = hashlib.sha256(payload).hexdigest()
    rec = {"event": event, "hash": h, "prev": prev}
    chain.append(rec)
    return rec

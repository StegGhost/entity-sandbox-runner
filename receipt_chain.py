import os, json, hashlib

PRIVATE_KEY = "dev-private-key"

def _sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def _canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def verify_receipt(receipt):
    core = receipt["core"]
    raw = _canonical(core)
    h = _sha256(raw)

    if h != receipt["chain"]["hash"]:
        return False

    sig = _sha256(h + PRIVATE_KEY)
    return sig == receipt["signature"]

def verify_chain(path="receipts/"):
    files = sorted(os.listdir(path))
    prev = "GENESIS"

    for f in files:
        full_path = os.path.join(path, f)

        if os.path.getsize(full_path) == 0:
            continue

        try:
            with open(full_path) as fh:
                r = json.load(fh)
        except Exception:
            continue

        if r["chain"]["prev_hash"] != prev:
            raise Exception(f"CHAIN BROKEN at {f}")

        if not verify_receipt(r):
            raise Exception(f"SIGNATURE INVALID at {f}")

        prev = r["chain"]["hash"]

    return True

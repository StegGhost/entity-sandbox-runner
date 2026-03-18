
import os, json, hashlib

def _sha256(x): return hashlib.sha256(x.encode()).hexdigest()
def _canon(x): return json.dumps(x, sort_keys=True, separators=(",", ":"))

def verify(path="receipts"):
    files = sorted(os.listdir(path))
    prev = "GENESIS"

    for f in files:
        with open(os.path.join(path,f)) as fh:
            r = json.load(fh)

        core = r["core"]
        h = _sha256(_canon(core))

        if h != r["chain"]["hash"]:
            raise Exception("HASH MISMATCH")

        if r["chain"]["prev_hash"] != prev:
            raise Exception("CHAIN BROKEN")

        prev = h

    return True

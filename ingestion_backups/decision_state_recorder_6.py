
import json, hashlib, time, os

PRIVATE_KEY = os.getenv("DSR_PRIVATE_KEY", "dev-private-key")

def _sha256(x): return hashlib.sha256(x.encode()).hexdigest()
def _canon(x): return json.dumps(x, sort_keys=True, separators=(",", ":"))

def sign(core):
    raw = _canon(core)
    h = _sha256(raw)
    sig = _sha256(h + PRIVATE_KEY)
    return h, sig

class DecisionStateRecorder:
    def __init__(self, path="receipts"):
        self.path = path
        os.makedirs(path, exist_ok=True)

    def _last_hash(self):
        files = sorted(os.listdir(self.path))
        if not files: return "GENESIS"
        with open(os.path.join(self.path, files[-1])) as f:
            return json.load(f)["chain"]["hash"]

    def record(self, delta, state, authority, policy, validation):
        ts = int(time.time()*1000)

        core = {
            "delta": delta,
            "state_hash": _sha256(_canon(state)),
            "authority": authority,
            "policy_hash": _sha256(_canon(policy)),
            "validation": validation,
            "timestamp": ts
        }

        h, sig = sign(core)

        receipt = {
            "core": core,
            "signature": sig,
            "chain": {
                "prev_hash": self._last_hash(),
                "hash": h
            }
        }

        with open(f"{self.path}/{ts}.json","w") as f:
            json.dump(receipt, f, indent=2)

        return receipt

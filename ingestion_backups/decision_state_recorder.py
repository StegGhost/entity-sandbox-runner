import json, hashlib, time, os
from typing import Dict, Any

PRIVATE_KEY = os.getenv("DSR_PRIVATE_KEY", "dev-private-key")

def _sha256(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()

def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def sign_payload(payload: Dict) -> Dict:
    raw = _canonical(payload)
    h = _sha256(raw)
    sig = _sha256(h + PRIVATE_KEY)
    return {
        "hash": h,
        "signature": sig
    }

def verify_signature(payload: Dict, signature: str, expected_hash: str) -> bool:
    raw = _canonical(payload)
    h = _sha256(raw)
    if h != expected_hash:
        return False
    return _sha256(h + PRIVATE_KEY) == signature

class DecisionStateRecorder:

    def __init__(self, chain_dir: str = "receipts/"):
        self.chain_dir = chain_dir
        os.makedirs(chain_dir, exist_ok=True)

    def _get_last_hash(self) -> str:
        files = sorted(os.listdir(self.chain_dir))
        if not files:
            return "GENESIS"
        last_file = files[-1]
        with open(os.path.join(self.chain_dir, last_file)) as f:
            return json.load(f)["chain"]["hash"]

    def _state_hash(self, state: Dict) -> str:
        return _sha256(_canonical(state))

    def _policy_hash(self, policy: Dict) -> str:
        return _sha256(_canonical(policy))

    def _validate(self, delta, state, authority, policy) -> Dict:
        # 🔒 Replace with your BCAT / invariant engine
        # deterministic only
        allowed = True

        return {
            "allowed": allowed,
            "reason": "deterministic-pass" if allowed else "blocked"
        }

    def record_decision(
        self,
        delta: Dict,
        state: Dict,
        authority: Dict,
        policy: Dict
    ) -> Dict:

        timestamp = int(time.time() * 1000)

        state_hash = self._state_hash(state)
        policy_hash = self._policy_hash(policy)

        validation = self._validate(delta, state, authority, policy)

        receipt_core = {
            "delta": delta,
            "state_hash": state_hash,
            "authority": authority,
            "policy_hash": policy_hash,
            "validation": validation,
            "timestamp": timestamp
        }

        sig = sign_payload(receipt_core)

        prev_hash = self._get_last_hash()

        chain_payload = {
            "prev_hash": prev_hash,
            "hash": sig["hash"]
        }

        full_receipt = {
            "core": receipt_core,
            "signature": sig["signature"],
            "chain": chain_payload
        }

        filename = f"{timestamp}.json"
        path = os.path.join(self.chain_dir, filename)

        with open(path, "w") as f:
            json.dump(full_receipt, f, indent=2)

        return full_receipt

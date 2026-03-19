import json
import hashlib
import time


def _hash(obj):
    raw = json.dumps(obj, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def build_experience(state_before, state_after, delta, uncertainty, policy_hash, parent=None):
    exp = {
        "timestamp": time.time(),
        "state_before": state_before,
        "state_after": state_after,
        "delta": delta,
        "uncertainty": uncertainty,
        "policy_hash": policy_hash,
        "parent": parent,
    }
    exp["hash"] = _hash(exp)
    return exp


def summarize(exp):
    return {
        "hash": exp["hash"],
        "uncertainty": exp["uncertainty"],
        "delta": exp["delta"],
        "policy": exp["policy_hash"],
    }

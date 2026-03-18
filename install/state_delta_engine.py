
import os, json, hashlib

GOV_PATHS = ["install", "config", "experiments"]

def _hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def _collect_files():
    files = []
    for root in GOV_PATHS:
        if not os.path.exists(root):
            continue
        for r,_,fs in os.walk(root):
            for f in fs:
                p = os.path.join(r,f)
                files.append(p)
    return sorted(files)

def state_hash():
    items = []
    for f in _collect_files():
        h = _hash_file(f)
        if h:
            items.append(f"{f}:{h}")
    raw = "\n".join(items)
    return hashlib.sha256(raw.encode()).hexdigest(), items

def delta_hash(before_items, after_items):
    raw = "\n".join(before_items + ["---"] + after_items)
    return hashlib.sha256(raw.encode()).hexdigest()

def uncertainty(before_items, after_items):
    # simple proxy: proportion changed
    before = set(before_items)
    after = set(after_items)
    diff = before.symmetric_difference(after)
    if len(before) == 0:
        return 0.0
    return len(diff) / len(before)

def compute_transition(before_items, after_items):
    sh_before = hashlib.sha256("\n".join(before_items).encode()).hexdigest()
    sh_after = hashlib.sha256("\n".join(after_items).encode()).hexdigest()
    dh = delta_hash(before_items, after_items)
    u = uncertainty(before_items, after_items)

    return {
        "state_before": sh_before,
        "state_after": sh_after,
        "delta": dh,
        "uncertainty": u
    }

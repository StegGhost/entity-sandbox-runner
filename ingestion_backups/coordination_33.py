import random

AVAILABLE_WORKERS = ["w1", "w2", "w3"]

def initialize_workers(state):
    workers = state.setdefault("workers", {})
    for w in AVAILABLE_WORKERS:
        workers.setdefault(w, {"score": 0.5, "count": 0, "failures": 0})

def select_worker(state):
    initialize_workers(state)
    workers = state["workers"]

    # epsilon-greedy exploration
    if random.random() < 0.20:
        return random.choice(list(workers.keys()))

    return max(workers.items(), key=lambda x: x[1].get("score", 0.5))[0]

def reassign_if_failed(state, result):
    if result["decision"] != "fail":
        return result["worker"]

    state.setdefault("failures", []).append({
        "shard": result["shard"],
        "confidence": result["confidence"],
        "worker": result["worker"],
    })

    # pick a fallback worker different from original if possible
    fallback_pool = [w for w in AVAILABLE_WORKERS if w != result["worker"]]
    return random.choice(fallback_pool) if fallback_pool else "w_fallback"

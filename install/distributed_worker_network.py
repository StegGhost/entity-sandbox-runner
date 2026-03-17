import time
workers = {}

def register(worker_id):
    workers[worker_id] = {"last_seen": time.time(), "score": 1.0}
    return workers[worker_id]

def heartbeat(worker_id):
    if worker_id in workers:
        workers[worker_id]["last_seen"] = time.time()
    return workers.get(worker_id)

def health(worker_id):
    w = workers.get(worker_id, {})
    return {"alive": (time.time() - w.get("last_seen", 0)) < 10, "score": w.get("score", 0)}

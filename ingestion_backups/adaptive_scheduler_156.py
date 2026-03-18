# adaptive_scheduler.py (patched for shared state)

from install.system_state import QUEUE

def add_shard(shard):
    QUEUE.append(shard)

def select_worker(workers):
    if not workers:
        return None
    # pick highest score
    return max(workers, key=lambda w: workers[w].get("score", 0))

def next_assignment(workers):
    if not QUEUE:
        return None
    shard = QUEUE.pop(0)
    worker = select_worker(workers)
    if not worker:
        return None
    return {"worker": worker, "shard": shard}

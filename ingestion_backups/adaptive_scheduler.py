queue = []

def add_shard(shard):
    queue.append(shard)

def select_worker(workers):
    # pick highest score
    return max(workers, key=lambda w: workers[w].get("score", 0)) if workers else None

def next_assignment(workers):
    if not queue:
        return None
    shard = queue.pop(0)
    worker = select_worker(workers)
    return {"worker": worker, "shard": shard}

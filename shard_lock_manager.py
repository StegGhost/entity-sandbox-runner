import os

def lock_shard(shard_id):
    path = f"locks/shard_{shard_id}.lock"
    if os.path.exists(path):
        return False

    open(path, "w").close()
    return True

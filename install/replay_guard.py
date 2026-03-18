import os

LOCK_FILE = "logs/lock"

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        raise Exception("REPLAY DETECTED")
    open(LOCK_FILE, "w").close()

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

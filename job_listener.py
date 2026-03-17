import os
import json

QUEUE_PATH = "job_queue/jobs"

def get_next_job():
    files = os.listdir(QUEUE_PATH)

    if not files:
        return None

    file = files[0]
    path = os.path.join(QUEUE_PATH, file)

    with open(path) as f:
        job = json.load(f)

    os.remove(path)
    return job

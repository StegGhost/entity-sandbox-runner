import time
from job_listener import get_next_job
from executor import run_job
from result_signer import sign_result

def worker_loop():
    while True:
        job = get_next_job()

        if not job:
            time.sleep(2)
            continue

        result = run_job(job)
        signed = sign_result(result)

        print(f"[WORKER] Completed job {job['shard']}")

if __name__ == "__main__":
    worker_loop()

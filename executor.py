import subprocess
import json

def run_job(job):
    experiment = job["experiment"]

    subprocess.run([
        "python",
        f"experiments/{experiment}/run_experiment.py",
    ])

    return {
        "experiment": experiment,
        "shard": job["shard"]
    }

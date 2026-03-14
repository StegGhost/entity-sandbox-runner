from pathlib import Path
from orchestrator import run_experiment

def run_all():

    experiments = Path("experiments")

    for exp in experiments.rglob("config.yaml"):

        exp_dir = exp.parent

        print("Running:", exp_dir)

        run_experiment(exp_dir)

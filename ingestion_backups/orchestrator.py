import argparse
from pathlib import Path
from scenario_loader import load_scenario
from result_writer import write_results
from handoff import build_handoff_manifest

ROOT = Path(__file__).resolve().parents[1]

def run_experiment(exp_path):

    scenario = load_scenario(exp_path)

    receipts = []
    state = scenario["initial_state"]

    for step in range(scenario["steps"]):

        proposal = scenario["transition"](state)

        admissible = proposal["a_next"] <= (
            scenario["K"]
            * proposal["g_next"] ** scenario["alpha"]
            * proposal["c_next"] ** scenario["beta"]
            * proposal["t_next"] ** scenario["gamma"]
        )

        receipt = {
            "step": step,
            "proposal": proposal,
            "admissible": admissible,
        }

        receipts.append(receipt)

        if admissible:
            state = proposal

    result = {
        "experiment": exp_path.name,
        "steps": len(receipts),
        "receipts": receipts,
        "final_state": state,
    }

    write_results(exp_path, result)
    manifest = build_handoff_manifest(exp_path, result)

    return manifest

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True)

    args = parser.parse_args()

    exp_path = ROOT / args.experiment
    manifest = run_experiment(exp_path)

    print(manifest)

if __name__ == "__main__":
    main()
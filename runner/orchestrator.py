import argparse
from pathlib import Path
from runner.scenario_loader import load_scenario
from runner.result_writer import write_results
from runner.handoff import build_handoff_manifest
from runner.receipts import write_receipts

ROOT = Path(__file__).resolve().parents[1]

def run_experiment(exp_path: Path) -> dict:
    scenario = load_scenario(exp_path)
    exp_name = scenario["experiment_id"]
    state = dict(scenario["initial_state"])
    receipts = []
    states = []

    for step in range(scenario["steps"]):
        proposal = scenario["transition"](state)
        admissible = proposal["a_next"] <= proposal["bound"]

        receipts.append({
            "experiment_id": exp_name,
            "step": step,
            "event_type": "state_transition_evaluated",
            "captured_data": [{
                "record_type": "admissibility_observation",
                "record_path": "data_records/canonical/admissibility_observations.jsonl",
                "record_id": f"{exp_name}_obs_{step:04d}",
            }],
            "math_relevance": ["GCAT.admissibility_bound"],
            "proposal": proposal,
            "admissible": admissible,
        })

        state_snapshot = {
            "step": step,
            "a_next": proposal["a_next"],
            "g_next": proposal["g_next"],
            "c_next": proposal["c_next"],
            "t_next": proposal["t_next"],
            "bound": proposal["bound"],
            "admissible": admissible,
        }
        states.append(state_snapshot)

        if admissible:
            state = {
                "a": proposal["a_next"],
                "g": proposal["g_next"],
                "c": proposal["c_next"],
                "t": proposal["t_next"],
            }

    result = {
        "experiment": exp_name,
        "steps": len(states),
        "receipts": [{"step": s["step"], "proposal": s, "admissible": s["admissible"]} for s in states],
        "trajectory": states,
        "final_state": state,
    }

    result_path = write_results(exp_name, result)
    write_receipts(exp_name, receipts)
    build_handoff_manifest(exp_name, str(result_path))
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", required=True, help="relative path to experiment folder")
    args = parser.parse_args()
    exp_path = ROOT / args.experiment
    result = run_experiment(exp_path)
    print(f"Experiment complete: {result['experiment']} steps={result['steps']}")

if __name__ == "__main__":
    main()

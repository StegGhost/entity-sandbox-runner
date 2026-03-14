import json
from pathlib import Path


def write_results(exp_path, result):

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    output = results_dir / f"{exp_path.name}_results.json"

    with open(output, "w") as f:
        json.dump(result, f, indent=2)

    return output

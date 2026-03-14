from pathlib import Path
import json

def write_results(exp_name: str, result: dict) -> Path:
    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)
    out = results_dir / f"{exp_name}_results.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return out

from pathlib import Path
import json

def write_summary_report(exp_name: str, result: dict) -> str:
    out_dir = Path("reports/latest")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{exp_name}_summary.md"

    trajectory = result.get("trajectory", [])
    admissible_count = sum(1 for t in trajectory if t["admissible"])
    inadmissible_count = len(trajectory) - admissible_count

    text = f"""# Experiment Summary: {exp_name}

- Steps: `{len(trajectory)}`
- Admissible steps: `{admissible_count}`
- Inadmissible steps: `{inadmissible_count}`

## Final State

```json
{json.dumps(result.get("final_state", {}), indent=2)}
```

## Data derivation

This report is derived from:
- `results/{exp_name}_results.json`
- `receipts/runs/{exp_name}_receipts.jsonl`
- canonical observations appended to `data_records/canonical/admissibility_observations.jsonl`

The report is a readable derivative artifact and not the canonical evidence layer.
"""
    path.write_text(text, encoding="utf-8")
    return str(path)

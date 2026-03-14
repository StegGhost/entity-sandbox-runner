from pathlib import Path
from datetime import datetime, timezone
import json

def append_admissibility_observations(exp_name: str, result: dict) -> int:
    out = Path("data_records/canonical/admissibility_observations.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with open(out, "a", encoding="utf-8") as f:
        for row in result.get("trajectory", []):
            payload = {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "experiment": exp_name,
                "step": row["step"],
                "a_next": row["a_next"],
                "g_next": row["g_next"],
                "c_next": row["c_next"],
                "t_next": row["t_next"],
                "bound": row["bound"],
                "admissible": row["admissible"],
                "source_results_file": f"results/{exp_name}_results.json",
            }
            f.write(json.dumps(payload) + "\n")
            count += 1
    return count

from pathlib import Path
import json

def rebuild_admissibility_stats() -> dict:
    src = Path("data_records/canonical/admissibility_observations.jsonl")
    out = Path("data_records/aggregates/admissibility_stats.json")
    out.parent.mkdir(parents=True, exist_ok=True)

    total = admissible = inadmissible = 0
    if src.exists():
        with open(src, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                total += 1
                if row["admissible"]:
                    admissible += 1
                else:
                    inadmissible += 1

    stats = {
        "total_observations": total,
        "admissible_observations": admissible,
        "inadmissible_observations": inadmissible,
        "inadmissible_fraction": 0 if total == 0 else inadmissible / total,
    }
    out.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    return stats

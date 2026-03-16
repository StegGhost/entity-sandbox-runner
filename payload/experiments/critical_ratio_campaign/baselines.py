import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "results" / "phase_space_map.json").read_text(encoding="utf-8"))

def safe_div(a, b):
    if b in (0, None):
        return None
    return a / b

def separation(values_stable, values_unstable):
    if not values_stable or not values_unstable:
        return None
    return abs((sum(values_stable)/len(values_stable)) - (sum(values_unstable)/len(values_unstable)))

stable = [d for d in DATA if d.get("viability_margin", 0) > 0]
unstable = [d for d in DATA if d.get("viability_margin", 0) <= 0]

rankings = {
    "capacity_over_pressure": separation(
        [safe_div(d["capacity"], d["pressure"]) for d in stable if safe_div(d["capacity"], d["pressure"]) is not None],
        [safe_div(d["capacity"], d["pressure"]) for d in unstable if safe_div(d["capacity"], d["pressure"]) is not None]
    ),
    "capacity_over_pressure_times_constraints": separation(
        [safe_div(d["capacity"], d["pressure"] * d["constraints"]) for d in stable if safe_div(d["capacity"], d["pressure"] * d["constraints"]) is not None],
        [safe_div(d["capacity"], d["pressure"] * d["constraints"]) for d in unstable if safe_div(d["capacity"], d["pressure"] * d["constraints"]) is not None]
    ),
    "capacity_times_continuity_over_pressure": separation(
        [safe_div(d["capacity"] * d["continuity"], d["pressure"]) for d in stable if safe_div(d["capacity"] * d["continuity"], d["pressure"]) is not None],
        [safe_div(d["capacity"] * d["continuity"], d["pressure"]) for d in unstable if safe_div(d["capacity"] * d["continuity"], d["pressure"]) is not None]
    ),
    "U": separation(
        [d["U"] for d in stable if d.get("U") is not None],
        [d["U"] for d in unstable if d.get("U") is not None]
    )
}

(ROOT / "results" / "baseline_comparison.json").write_text(json.dumps(rankings, indent=2), encoding="utf-8")
print(json.dumps(rankings, indent=2))

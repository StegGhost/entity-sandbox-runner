import json
from pathlib import Path

RESULTS = Path("results/phase_space_map.json")
OUTPUT = Path("results/baseline_comparison.json")

def safe_div(a, b):
    return None if b in (0, None) else a / b

def score(data, key_fn):
    stable_vals = []
    unstable_vals = []
    for d in data:
        val = key_fn(d)
        if val is None:
            continue
        if d.get("viability_margin", 0) > 0:
            stable_vals.append(val)
        else:
            unstable_vals.append(val)
    if not stable_vals or not unstable_vals:
        return None
    return abs((sum(stable_vals)/len(stable_vals)) - (sum(unstable_vals)/len(unstable_vals)))

def main():
    data = json.loads(RESULTS.read_text())
    rankings = {
        "capacity_over_pressure": score(data, lambda d: safe_div(d.get("capacity"), d.get("pressure"))),
        "capacity_over_pressure_times_constraints": score(data, lambda d: safe_div(d.get("capacity"), (d.get("pressure") or 0) * (d.get("constraints") or 0))),
        "capacity_times_continuity_over_pressure": score(data, lambda d: safe_div((d.get("capacity") or 0) * (d.get("continuity") or 0), d.get("pressure"))),
        "U": score(data, lambda d: d.get("U")),
    }
    OUTPUT.write_text(json.dumps(rankings, indent=2))
    print(json.dumps(rankings, indent=2))

if __name__ == "__main__":
    main()

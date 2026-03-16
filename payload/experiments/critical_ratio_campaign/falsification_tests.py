import json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"

def compute_u_star(capacity, pressure, constraints, continuity, drift):
    denom = (pressure * constraints) + drift
    if denom == 0:
        return None
    return (capacity * continuity) / denom

trials = []
for _ in range(5000):
    capacity = random.uniform(0.1, 5.0)
    pressure = random.uniform(0.1, 5.0)
    constraints = random.uniform(0.1, 5.0)
    continuity = random.uniform(0.1, 5.0)
    drift = random.uniform(0.0, 1.0)
    u_star = compute_u_star(capacity, pressure, constraints, continuity, drift)
    viability_margin = (capacity * continuity) - ((pressure * constraints) + drift)
    trials.append({"U_star": u_star, "viability_margin": viability_margin})

boundary = [x["U_star"] for x in trials if x["U_star"] is not None and abs(x["viability_margin"]) < 0.05]
report = {
    "trial_count": len(trials),
    "boundary_count": len(boundary),
    "mean_boundary_U_star": (sum(boundary) / len(boundary)) if boundary else None,
    "note": "Explores whether a drift-corrected invariant fits better under perturbation."
}
(RESULTS / "falsification_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))

import json, random
from pathlib import Path

OUTPUT = Path("results/falsification_report.json")

def compute_u(capacity, pressure, constraints, continuity, drift=0.0):
    denom = (pressure * constraints) + drift
    return None if denom == 0 else (capacity * continuity) / denom

def main():
    trials = []
    for _ in range(5000):
        c = random.uniform(0.1, 5)
        p = random.uniform(0.1, 5)
        k = random.uniform(0.1, 5)
        t = random.uniform(0.1, 5)
        drift = random.uniform(0.0, 1.0)
        u = compute_u(c, p, k, t, drift=drift)
        v = (c * t) - ((p * k) + drift)
        trials.append({
            "U_star": u,
            "viability_margin": v
        })
    boundary = [x["U_star"] for x in trials if x["U_star"] is not None and abs(x["viability_margin"]) < 0.05]
    report = {
        "trial_count": len(trials),
        "boundary_count": len(boundary),
        "mean_boundary_U_star": (sum(boundary) / len(boundary)) if boundary else None,
        "note": "Tests whether a drift-corrected invariant may fit better than the baseline U."
    }
    OUTPUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()

import json, random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

def viability(capacity, pressure, constraints, continuity):
    return (capacity * continuity) - (pressure * constraints)

def compute_u(capacity, pressure, constraints, continuity):
    denom = pressure * constraints
    return None if denom == 0 else (capacity * continuity) / denom

data = []
boundary = []
for _ in range(200000):
    capacity = random.uniform(0.1, 5.0)
    pressure = random.uniform(0.1, 5.0)
    constraints = random.uniform(0.1, 5.0)
    continuity = random.uniform(0.1, 5.0)

    v = viability(capacity, pressure, constraints, continuity)
    u = compute_u(capacity, pressure, constraints, continuity)
    row = {
        "capacity": capacity,
        "pressure": pressure,
        "constraints": constraints,
        "continuity": continuity,
        "viability_margin": v,
        "U": u
    }
    data.append(row)
    if u is not None and abs(v) < 0.02:
        boundary.append(row)

(RESULTS / "phase_space_map.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
(RESULTS / "collapse_boundary_surface.json").write_text(json.dumps(boundary, indent=2), encoding="utf-8")
print("Expanded experiment completed")

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "results" / "phase_space_map.json").read_text(encoding="utf-8"))

stable = [d for d in DATA if d["viability_margin"] > 0]
unstable = [d for d in DATA if d["viability_margin"] <= 0]
boundary = [d["U"] for d in DATA if d.get("U") is not None and abs(d.get("viability_margin", 0)) < 0.05]

print("Stable states:", len(stable))
print("Unstable states:", len(unstable))
if boundary:
    print("Estimated critical Uc:", sum(boundary) / len(boundary))

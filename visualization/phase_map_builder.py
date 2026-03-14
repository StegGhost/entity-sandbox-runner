import json
from pathlib import Path
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

def build_phase_map(dataset_path="datasets/collapse_curve.json"):
    p = Path(dataset_path)
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    ratios = [d["ratio"] for d in data]
    collapse = [1 if d["collapse"] else 0 for d in data]
    reports = Path("reports")
    reports.mkdir(parents=True, exist_ok=True)
    if plt is None:
        return None
    plt.figure()
    plt.scatter(ratios, collapse)
    plt.xlabel("Adversarial Ratio")
    plt.ylabel("Collapse State")
    plt.title("GCAT Phase Map")
    out = reports / "phase_map_live.png"
    plt.savefig(out)
    plt.close()
    return str(out)

import json
from pathlib import Path

CONFIG = Path("expected_outputs.json")
RESULTS = Path("results/phase_space_map.json")
REPORT = Path("results/validation_report.json")

def main():
    expected = json.loads(CONFIG.read_text())
    data = json.loads(RESULTS.read_text())

    sample_count = len(data)
    stable_count = sum(1 for d in data if d.get("viability_margin", 0) > 0)
    unstable_count = sum(1 for d in data if d.get("viability_margin", 0) <= 0)
    boundary = [d.get("U") for d in data if abs(d.get("viability_margin", 0)) < 0.05 and d.get("U") is not None]
    critical_uc = (sum(boundary) / len(boundary)) if boundary else None

    checks = expected["expected"]
    result = {
        "sample_count": sample_count,
        "stable_count": stable_count,
        "unstable_count": unstable_count,
        "critical_Uc": critical_uc,
        "sample_count_ok": sample_count >= checks["sample_count"],
        "stable_count_ok": checks["stable_count_range"][0] <= stable_count <= checks["stable_count_range"][1],
        "unstable_count_ok": checks["unstable_count_range"][0] <= unstable_count <= checks["unstable_count_range"][1],
        "critical_Uc_ok": critical_uc is not None and checks["critical_Uc_range"][0] <= critical_uc <= checks["critical_Uc_range"][1]
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

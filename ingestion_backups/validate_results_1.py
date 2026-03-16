import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXPECTED = json.loads((ROOT / "expected_outputs.json").read_text(encoding="utf-8"))
DATA = json.loads((ROOT / "results" / "phase_space_map.json").read_text(encoding="utf-8"))

sample_count = len(DATA)
boundary = [d["U"] for d in DATA if d.get("U") is not None and abs(d.get("viability_margin", 0)) < 0.05]
critical_uc = (sum(boundary) / len(boundary)) if boundary else None

report = {
    "sample_count": sample_count,
    "critical_Uc": critical_uc,
    "sample_count_ok": sample_count >= EXPECTED["expected"]["minimum_sample_count"],
    "critical_Uc_ok": critical_uc is not None and EXPECTED["expected"]["critical_Uc_range"][0] <= critical_uc <= EXPECTED["expected"]["critical_Uc_range"][1]
}

(ROOT / "results" / "validation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))

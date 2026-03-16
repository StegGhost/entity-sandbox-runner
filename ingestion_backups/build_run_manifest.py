import json
from pathlib import Path

EXP_ROOT = Path("experiments/critical_ratio_campaign")
RESULTS = EXP_ROOT / "results"
OUTPUT = RESULTS / "run_manifest.json"

def main():
    data = json.loads((RESULTS / "phase_space_map.json").read_text(encoding="utf-8"))
    validation = {}
    if (RESULTS / "validation_report.json").exists():
        validation = json.loads((RESULTS / "validation_report.json").read_text(encoding="utf-8"))

    stable = sum(1 for d in data if d.get("viability_margin", 0) > 0)
    unstable = sum(1 for d in data if d.get("viability_margin", 0) <= 0)

    manifest = {
        "run_id": "critical_ratio_campaign_latest",
        "experiment": "critical_ratio_campaign",
        "sample_count": len(data),
        "stable_states": stable,
        "unstable_states": unstable,
        "estimated_Uc": validation.get("critical_Uc"),
        "validation_passed": validation.get("critical_Uc_ok", False) and validation.get("sample_count_ok", False)
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()

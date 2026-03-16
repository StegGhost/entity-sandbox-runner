import json
from pathlib import Path

EXP_ROOT = Path("experiments/critical_ratio_campaign")
RESULTS = EXP_ROOT / "results"
PUBLISHED = EXP_ROOT / "published" / "latest"
PUBLISHED.mkdir(parents=True, exist_ok=True)

manifest = json.loads((RESULTS / "run_manifest.json").read_text(encoding="utf-8"))
summary = {
    "experiment": manifest["experiment"],
    "run_id": manifest["run_id"],
    "sample_count": manifest["sample_count"],
    "stable_states": manifest["stable_states"],
    "unstable_states": manifest["unstable_states"],
    "estimated_Uc": manifest["estimated_Uc"],
    "validation_passed": manifest["validation_passed"]
}
(PUBLISHED / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
md = (
    "# Latest Critical Ratio Campaign Result\n\n"
    f"- Sample count: {summary['sample_count']}\n"
    f"- Stable states: {summary['stable_states']}\n"
    f"- Unstable states: {summary['unstable_states']}\n"
    f"- Estimated Uc: {summary['estimated_Uc']}\n"
    f"- Validation passed: {summary['validation_passed']}\n"
)
(PUBLISHED / "summary.md").write_text(md, encoding="utf-8")
print((PUBLISHED / "summary.json"))

import zipfile
from pathlib import Path

EXP_ROOT = Path("experiments/critical_ratio_campaign")
RESULTS = EXP_ROOT / "results"
ARTIFACTS = EXP_ROOT / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)

include = [
    EXP_ROOT / "README.md",
    EXP_ROOT / "CLAIMS.md",
    EXP_ROOT / "protocol.md",
    EXP_ROOT / "experiment_config.json",
    RESULTS / "validation_report.json",
    RESULTS / "baseline_comparison.json",
    RESULTS / "falsification_report.json",
    RESULTS / "run_manifest.json",
]

out = ARTIFACTS / "critical_ratio_campaign_standard.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in include:
        if p.exists():
            z.write(p, p.relative_to(EXP_ROOT))
print(out)

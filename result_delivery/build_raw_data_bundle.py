import zipfile, hashlib, json
from pathlib import Path

EXP_ROOT = Path("experiments/critical_ratio_campaign")
RESULTS = EXP_ROOT / "results"
RAW = EXP_ROOT / "raw_exports"
RAW.mkdir(parents=True, exist_ok=True)

out = RAW / "critical_ratio_campaign_raw.zip"
included = []
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in [
        RESULTS / "phase_space_map.json",
        RESULTS / "validation_report.json",
        RESULTS / "baseline_comparison.json",
        RESULTS / "falsification_report.json",
        RESULTS / "run_manifest.json",
    ]:
        if p.exists():
            z.write(p, p.relative_to(EXP_ROOT))
            included.append(str(p.relative_to(EXP_ROOT)))

sha = hashlib.sha256(out.read_bytes()).hexdigest()
meta = {
    "archive_name": out.name,
    "included_files": included,
    "sha256": sha,
    "compressed_bytes": out.stat().st_size
}
(RAW / "critical_ratio_campaign_raw.meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
print(json.dumps(meta, indent=2))

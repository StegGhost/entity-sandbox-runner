from pathlib import Path
import json, zipfile

ROOT = Path("experiments/critical_ratio_campaign")
RESULTS = ROOT / "results"
OUTDIR = ROOT / "exports"

def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    bundle = OUTDIR / "critical_ratio_campaign_export.zip"
    included = []
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
        for p in [
            RESULTS / "phase_space_map.json",
            RESULTS / "merge_summary.json",
            RESULTS / "validation_report.json",
        ]:
            if p.exists():
                z.write(p, p.relative_to(ROOT))
                included.append(str(p.relative_to(ROOT)))
    meta = {"bundle": bundle.name, "included": included}
    (OUTDIR / "critical_ratio_campaign_export.meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()

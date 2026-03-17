from pathlib import Path
import json

ROOT = Path("experiments/critical_ratio_campaign")
RESULTS = ROOT / "results"
PUB = ROOT / "published" / "latest"

def main():
    PUB.mkdir(parents=True, exist_ok=True)
    merge_summary = {}
    p = RESULTS / "merge_summary.json"
    if p.exists():
        merge_summary = json.loads(p.read_text(encoding="utf-8"))
    summary = {
        "experiment": "critical_ratio_campaign",
        "merged_samples": merge_summary.get("merged_samples"),
        "estimated_Uc": merge_summary.get("estimated_Uc"),
        "stable_count": merge_summary.get("stable_count"),
        "unstable_count": merge_summary.get("unstable_count"),
        "status": merge_summary.get("status", "unknown"),
    }
    (PUB / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    md = (
        "# Critical Ratio Campaign\n\n"
        f"- Merged samples: {summary['merged_samples']}\n"
        f"- Estimated Uc: {summary['estimated_Uc']}\n"
        f"- Stable count: {summary['stable_count']}\n"
        f"- Unstable count: {summary['unstable_count']}\n"
        f"- Status: {summary['status']}\n"
    )
    (PUB / "summary.md").write_text(md, encoding="utf-8")
    print((PUB / "summary.json"))

if __name__ == "__main__":
    main()

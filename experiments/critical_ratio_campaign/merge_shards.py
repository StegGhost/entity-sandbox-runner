from __future__ import annotations

import json
from pathlib import Path
from statistics import mean


def main() -> None:
    root = Path(__file__).resolve().parent
    results_dir = root / "results"
    shards_dir = results_dir / "shards"
    results_dir.mkdir(parents=True, exist_ok=True)
    shards_dir.mkdir(parents=True, exist_ok=True)

    merged: list[dict] = []
    shard_files = sorted(shards_dir.glob("shard_*.json"))

    if not shard_files:
        raise FileNotFoundError(f"No shard files found in {shards_dir}")

    for shard_file in shard_files:
        try:
            payload = json.loads(shard_file.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                merged.extend(payload)
            else:
                print(f"Skipping {shard_file}: expected list, got {type(payload).__name__}")
        except Exception as exc:
            print(f"Skipping {shard_file}: {exc}")

    out = results_dir / "phase_space_map.json"
    out.write_text(json.dumps(merged, indent=2), encoding="utf-8")

    stable_count = sum(1 for row in merged if row.get("stable") is True or row.get("viability_margin", 0) > 0)
    unstable_count = len(merged) - stable_count
    boundary = [
        row.get("U")
        for row in merged
        if row.get("U") is not None and abs(row.get("viability_margin", 0)) < 0.05
    ]

    summary = {
        "merged_samples": len(merged),
        "shard_count": len(shard_files),
        "stable_count": stable_count,
        "unstable_count": unstable_count,
        "estimated_Uc": mean(boundary) if boundary else None,
        "output": str(out),
    }

    (results_dir / "merge_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

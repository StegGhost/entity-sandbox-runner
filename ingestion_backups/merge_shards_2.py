from __future__ import annotations

import json
from pathlib import Path
from statistics import mean


def safe_read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Skipping unreadable shard {path}: {exc}")
        return None


def atomic_write_json(path: Path, payload) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    root = Path(__file__).resolve().parent
    results_dir = root / "results"
    shards_dir = results_dir / "shards"
    logs_dir = results_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    shard_files = sorted(shards_dir.glob("shard_*.json"))
    if not shard_files:
        raise FileNotFoundError(f"No shard files found in {shards_dir}")

    merged = []
    shard_status = []
    failed_files = []

    for shard_file in shard_files:
        payload = safe_read_json(shard_file)
        if isinstance(payload, list):
            merged.extend(payload)
            shard_status.append({"file": str(shard_file), "status": "ok", "rows": len(payload)})
        else:
            failed_files.append(str(shard_file))
            shard_status.append({"file": str(shard_file), "status": "invalid"})

    out = results_dir / "phase_space_map.json"
    atomic_write_json(out, merged)

    stable_count = sum(1 for row in merged if row.get("stable") is True or row.get("margin", 0) > 0)
    unstable_count = len(merged) - stable_count
    boundary = [row.get("U") for row in merged if row.get("U") is not None and abs(row.get("margin", 0)) < 0.05]

    summary = {
        "status": "ok" if not failed_files else "partial",
        "merged_samples": len(merged),
        "shard_count": len(shard_files),
        "failed_files": failed_files,
        "stable_count": stable_count,
        "unstable_count": unstable_count,
        "estimated_Uc": mean(boundary) if boundary else None,
        "output": str(out),
    }

    atomic_write_json(results_dir / "merge_summary.json", summary)
    atomic_write_json(logs_dir / "merge_health.json", {
        "status": summary["status"],
        "shards_seen": len(shard_files),
        "failed_files": failed_files,
    })
    atomic_write_json(logs_dir / "merge_shard_status.json", shard_status)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import random
import sys
import traceback
from pathlib import Path
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Critical Ratio Campaign runner")
    parser.add_argument("--runs", type=int, default=50000, help="Number of samples for this run/shard")
    parser.add_argument("--shard", type=int, default=0, help="Shard index")
    parser.add_argument("--total-shards", type=int, default=1, help="Total shards")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic seed")
    parser.add_argument("--adaptive", action="store_true", help="Bias samples near boundary U≈1")
    return parser.parse_args()


def compute_u(capacity: float, pressure: float, constraints: float, continuity: float):
    denom = pressure * constraints
    if denom == 0:
        return None
    return (capacity * continuity) / denom


def viability_margin(capacity: float, pressure: float, constraints: float, continuity: float) -> float:
    return (capacity * continuity) - (pressure * constraints)


def sample_uniform(rng: random.Random):
    return (
        rng.uniform(0.1, 5.0),
        rng.uniform(0.1, 5.0),
        rng.uniform(0.1, 5.0),
        rng.uniform(0.1, 5.0),
    )


def sample_adaptive(rng: random.Random):
    capacity = rng.uniform(0.25, 4.5)
    pressure = rng.uniform(0.25, 4.5)
    constraints = rng.uniform(0.25, 4.5)

    target_ratio = 1.0 + rng.uniform(-0.08, 0.08)
    continuity = (target_ratio * pressure * constraints) / max(capacity, 1e-9)
    continuity = max(0.1, min(5.0, continuity + rng.uniform(-0.05, 0.05)))
    return capacity, pressure, constraints, continuity


def build_row(capacity: float, pressure: float, constraints: float, continuity: float, shard: int, sample_id: int):
    u = compute_u(capacity, pressure, constraints, continuity)
    margin = viability_margin(capacity, pressure, constraints, continuity)
    return {
        "sample_id": sample_id,
        "shard": shard,
        "capacity": capacity,
        "pressure": pressure,
        "constraints": constraints,
        "continuity": continuity,
        "U": u,
        "margin": margin,
        "stable": margin > 0,
    }


def atomic_write_json(path: Path, payload) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    args = parse_args()

    root = Path(__file__).resolve().parent
    results_dir = root / "results"
    shards_dir = results_dir / "shards"
    logs_dir = results_dir / "logs"

    results_dir.mkdir(parents=True, exist_ok=True)
    shards_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    shard_path = shards_dir / f"shard_{args.shard}.json"
    summary_path = results_dir / f"shard_{args.shard}_summary.json"
    health_path = logs_dir / f"shard_{args.shard}_health.json"
    error_path = logs_dir / f"shard_{args.shard}_error.log"

    rng = random.Random(args.seed)

    rows = []
    skipped = 0
    failures = 0

    try:
        for i in range(args.runs):
            try:
                if args.adaptive:
                    capacity, pressure, constraints, continuity = sample_adaptive(rng)
                else:
                    capacity, pressure, constraints, continuity = sample_uniform(rng)

                denom = pressure * constraints
                if denom == 0:
                    skipped += 1
                    continue

                rows.append(build_row(capacity, pressure, constraints, continuity, args.shard, i))
            except Exception:
                failures += 1
                continue

        atomic_write_json(shard_path, rows)

        if args.total_shards == 1:
            atomic_write_json(results_dir / "phase_space_map.json", rows)

        stable_count = sum(1 for row in rows if row["stable"])
        unstable_count = len(rows) - stable_count
        boundary = [row["U"] for row in rows if row["U"] is not None and abs(row["margin"]) < 0.05]

        summary = {
            "status": "ok",
            "runs_requested": args.runs,
            "rows_written": len(rows),
            "skipped": skipped,
            "row_failures": failures,
            "shard": args.shard,
            "total_shards": args.total_shards,
            "seed": args.seed,
            "adaptive": args.adaptive,
            "stable_count": stable_count,
            "unstable_count": unstable_count,
            "mean_boundary_U": mean(boundary) if boundary else None,
            "output": str(shard_path),
        }
        atomic_write_json(summary_path, summary)
        atomic_write_json(health_path, {
            "status": "ok",
            "shard": args.shard,
            "rows_written": len(rows),
            "row_failures": failures,
            "skipped": skipped,
        })

        print(json.dumps(summary, indent=2))
        return 0

    except Exception as exc:
        error_path.write_text(traceback.format_exc(), encoding="utf-8")
        atomic_write_json(health_path, {
            "status": "failed",
            "shard": args.shard,
            "error": repr(exc),
            "error_log": str(error_path),
        })
        print(f"Shard {args.shard} failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

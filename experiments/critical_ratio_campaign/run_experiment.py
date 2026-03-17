from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from statistics import mean


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Critical Ratio Campaign runner")
    parser.add_argument("--runs", type=int, default=50000, help="Number of samples to generate in this shard/run")
    parser.add_argument("--shard", type=int, default=0, help="Shard index for parallel runs")
    parser.add_argument("--total-shards", type=int, default=1, help="Total shard count")
    parser.add_argument("--seed", type=int, default=42, help="Deterministic RNG seed")
    parser.add_argument("--adaptive", action="store_true", help="Bias sampling toward the collapse boundary")
    return parser.parse_args()


def compute_u(capacity: float, pressure: float, constraints: float, continuity: float) -> float | None:
    denom = pressure * constraints
    if denom == 0:
        return None
    return (capacity * continuity) / denom


def viability_margin(capacity: float, pressure: float, constraints: float, continuity: float) -> float:
    return (capacity * continuity) - (pressure * constraints)


def sample_uniform(rng: random.Random) -> tuple[float, float, float, float]:
    return (
        rng.uniform(0.1, 5.0),
        rng.uniform(0.1, 5.0),
        rng.uniform(0.1, 5.0),
        rng.uniform(0.1, 5.0),
    )


def sample_adaptive(rng: random.Random) -> tuple[float, float, float, float]:
    # Concentrate more mass near the critical surface by anchoring three variables,
    # then solving the fourth to keep U close to 1 with a small perturbation.
    capacity = rng.uniform(0.25, 4.5)
    pressure = rng.uniform(0.25, 4.5)
    constraints = rng.uniform(0.25, 4.5)

    target_ratio = 1.0 + rng.uniform(-0.08, 0.08)
    continuity = (target_ratio * pressure * constraints) / capacity

    # Clip back into the experiment box while preserving some adaptive bias.
    continuity = max(0.1, min(5.0, continuity))

    # Add a bit of jitter so the adaptive sampler still explores a band, not a line.
    continuity = max(0.1, min(5.0, continuity + rng.uniform(-0.05, 0.05)))

    return capacity, pressure, constraints, continuity


def build_row(capacity: float, pressure: float, constraints: float, continuity: float, shard: int, sample_id: int) -> dict:
    u = compute_u(capacity, pressure, constraints, continuity)
    v = viability_margin(capacity, pressure, constraints, continuity)
    return {
        "sample_id": sample_id,
        "shard": shard,
        "capacity": capacity,
        "pressure": pressure,
        "constraints": constraints,
        "continuity": continuity,
        "viability_margin": v,
        "U": u,
        "stable": v > 0,
    }


def main() -> None:
    args = parse_args()

    root = Path(__file__).resolve().parent
    results_dir = root / "results"
    shards_dir = results_dir / "shards"
    results_dir.mkdir(parents=True, exist_ok=True)
    shards_dir.mkdir(parents=True, exist_ok=True)

    rng = random.Random(args.seed)

    rows: list[dict] = []
    for i in range(args.runs):
        if args.adaptive:
            capacity, pressure, constraints, continuity = sample_adaptive(rng)
        else:
            capacity, pressure, constraints, continuity = sample_uniform(rng)

        rows.append(build_row(capacity, pressure, constraints, continuity, args.shard, i))

    shard_path = shards_dir / f"shard_{args.shard}.json"
    shard_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")

    # For single-run mode, also materialize the canonical phase_space_map.json
    if args.total_shards == 1:
        (results_dir / "phase_space_map.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")

    stable_count = sum(1 for row in rows if row["stable"])
    unstable_count = len(rows) - stable_count
    boundary = [row["U"] for row in rows if row["U"] is not None and abs(row["viability_margin"]) < 0.05]
    summary = {
        "runs": args.runs,
        "shard": args.shard,
        "total_shards": args.total_shards,
        "seed": args.seed,
        "adaptive": args.adaptive,
        "stable_count": stable_count,
        "unstable_count": unstable_count,
        "mean_boundary_U": mean(boundary) if boundary else None,
        "shard_output": str(shard_path),
    }

    (results_dir / f"shard_{args.shard}_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

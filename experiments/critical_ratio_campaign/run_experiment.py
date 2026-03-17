import argparse, json, random
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--runs", type=int, default=10000)
parser.add_argument("--shard", type=int, default=0)
parser.add_argument("--total-shards", type=int, default=1)
parser.add_argument("--seed", type=int, default=42)
args = parser.parse_args()

random.seed(args.seed)

results = []
for i in range(args.runs):
    capacity = random.uniform(0.1,5)
    pressure = random.uniform(0.1,5)
    constraints = random.uniform(0.1,5)
    continuity = random.uniform(0.1,5)

    denom = pressure * constraints
    U = (capacity * continuity)/denom if denom != 0 else None
    margin = (capacity*continuity) - denom

    results.append({
        "shard": args.shard,
        "sample": i,
        "U": U,
        "margin": margin
    })

out = Path("results/shards") / f"shard_{args.shard}.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(results))
print(f"Wrote {out}")
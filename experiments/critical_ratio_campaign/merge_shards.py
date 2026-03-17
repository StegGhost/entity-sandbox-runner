import json
from pathlib import Path

root = Path("results/shards")
merged = []

for f in root.glob("*.json"):
    merged.extend(json.loads(f.read_text()))

out = Path("results/phase_space_map.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(merged, indent=2))

print(f"Merged {len(merged)} samples")
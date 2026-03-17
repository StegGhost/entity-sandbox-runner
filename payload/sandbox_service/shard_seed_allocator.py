from pathlib import Path
import json

OUTPUT = Path("sandbox_service/shard_seed_allocator.json")

def main():
    payload = {
        "service_module": "shard_seed_allocator",
        "status": "ready",
        "note": "Allocates deterministic seeds across shards."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

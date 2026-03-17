from pathlib import Path
import json

OUTPUT = Path("cluster_plane/worker_capacity_registry.json")

def main():
    payload = {
        "cluster_module": "worker_capacity_registry",
        "status": "ready",
        "note": "Tracks cluster worker capacity and status."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

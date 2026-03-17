from pathlib import Path
import json

OUTPUT = Path("cluster_plane/compute_budget_allocator.json")

def main():
    payload = {
        "cluster_module": "compute_budget_allocator",
        "status": "ready",
        "note": "Allocates compute budget to distributed campaigns."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

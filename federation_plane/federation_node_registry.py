from pathlib import Path
import json

OUTPUT = Path("federation_plane/federation_node_registry.json")

def main():
    payload = {
        "federation_module": "federation_node_registry",
        "status": "ready",
        "note": "Registers federation nodes and capabilities."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

from pathlib import Path
import json

OUTPUT = Path("publication_plane/demo_surface_sync_agent.json")

def main():
    payload = {
        "module": "demo_surface_sync_agent",
        "status": "initialized",
        "note": "Syncs latest summaries to the demo surface."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

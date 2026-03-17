from pathlib import Path
import json

OUTPUT = Path("cluster_plane/campaign_retry_controller.json")

def main():
    payload = {
        "cluster_module": "campaign_retry_controller",
        "status": "ready",
        "note": "Controls campaign retry behavior."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

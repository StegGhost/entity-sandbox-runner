from pathlib import Path
import json

OUTPUT = Path("sandbox_service/replication_job_board.json")

def main():
    payload = {
        "service_module": "replication_job_board",
        "status": "ready",
        "note": "Maintains a board of replication jobs."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

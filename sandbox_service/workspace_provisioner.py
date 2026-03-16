from pathlib import Path
import json

OUTPUT = Path("sandbox_service/workspace_provisioner.json")

def main():
    result = {
        "service_module": "workspace_provisioner",
        "status": "ready",
        "note": "Creates per-user or per-project sandbox workspaces."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()

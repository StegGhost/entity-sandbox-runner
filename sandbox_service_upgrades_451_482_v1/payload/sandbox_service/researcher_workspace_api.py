
from pathlib import Path
import json

OUTPUT = Path("sandbox_service/researcher_workspace_api.json")

def main():
    result = {
        "service_module": "researcher_workspace_api",
        "status": "ready"
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
    print(result)

if __name__ == "__main__":
    main()

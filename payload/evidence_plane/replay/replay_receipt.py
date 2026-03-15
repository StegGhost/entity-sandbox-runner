import json
from pathlib import Path

def replay_receipt(path: str):
    p = Path(path)
    with open(p, "r", encoding="utf-8") as f:
        receipt = json.load(f)
    files = receipt.get("files", {})
    return {
        "bundle": receipt.get("bundle"),
        "timestamp": receipt.get("timestamp"),
        "file_count": len(files),
        "files": files,
    }

if __name__ == "__main__":
    import sys
    print(json.dumps(replay_receipt(sys.argv[1]), indent=2))

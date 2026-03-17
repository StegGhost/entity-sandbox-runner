from pathlib import Path
import json

OUTPUT = Path("publication_plane/dataset_doi_stub.json")

def main():
    payload = {
        "module": "dataset_doi_stub",
        "status": "initialized",
        "note": "Roadmap scaffold for upgrade 867."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

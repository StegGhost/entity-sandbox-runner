from pathlib import Path
import json

OUTPUT = Path("sandbox_service/final_results_zip_builder.json")

def main():
    payload = {
        "module": "final_results_zip_builder",
        "status": "initialized",
        "note": "Builds downloadable final result bundles."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

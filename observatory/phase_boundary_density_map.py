from pathlib import Path
import json

OUTPUT = Path("observatory/phase_boundary_density_map.json")

def main():
    payload = {
        "module": "phase_boundary_density_map",
        "status": "initialized",
        "note": "Maps density near the detected phase boundary."
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

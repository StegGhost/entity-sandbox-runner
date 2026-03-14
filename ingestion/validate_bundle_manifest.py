from pathlib import Path
import json
import sys

REQUIRED_TOP = {"bundle_name", "bundle_version", "install_mode"}

def validate_manifest(path: str) -> int:
    p = Path(path)
    if not p.exists():
        print(f"missing manifest: {p}")
        return 1

    data = json.loads(p.read_text(encoding="utf-8"))

    missing = sorted(REQUIRED_TOP - set(data.keys()))
    if missing:
        print(f"missing required keys: {missing}")
        return 1

    mode = data["install_mode"]
    if mode not in {"file_map", "folder_map"}:
        print(f"invalid install_mode: {mode}")
        return 1

    if mode == "file_map" and "file_map" not in data:
        print("file_map mode requires file_map")
        return 1

    if mode == "folder_map" and "folder_map" not in data:
        print("folder_map mode requires folder_map")
        return 1

    print("manifest valid")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python ingestion/validate_bundle_manifest.py bundle_manifest.json")
        raise SystemExit(1)

    raise SystemExit(validate_manifest(sys.argv[1]))

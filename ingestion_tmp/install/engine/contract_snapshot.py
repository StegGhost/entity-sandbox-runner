import json, os, sys
from datetime import datetime, timezone

def detect_env():
    env = {
        "cwd": os.getcwd(),
        "python_version": sys.version,
        "env_keys": sorted(list(os.environ.keys()))[:50]
    }
    return env

def infer_rules():
    # Known/assumed signals from prior failures (kept explicit and transparent)
    return {
        "required_manifest_fields": ["bundle_name", "bundle_version", "version", "install_mode", "allowed_paths"],
        "allowed_root_paths": ["bundle_manifest.json", "install/engine/", "install/tests/"],
        "notes": [
            "This snapshot is generated inside allowed paths only.",
            "Workflows, docs, config, and root install scripts are not permitted in current ingestion mode."
        ]
    }

def main(out_path="ingestion_contract_snapshot.json"):
    snapshot = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "env": detect_env(),
        "inferred_rules": infer_rules(),
        "write_target": out_path
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)
    print(out_path)

if __name__ == "__main__":
    main()

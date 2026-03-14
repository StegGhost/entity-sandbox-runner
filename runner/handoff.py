from pathlib import Path
from datetime import datetime, timezone
import json

def build_handoff_manifest(exp_name: str, result_path: str, report_paths=None) -> dict:
    manifest = {
        "experiment_id": exp_name,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "result_file": result_path,
        "report_paths": report_paths or [],
    }
    manifests = Path("manifests")
    manifests.mkdir(parents=True, exist_ok=True)
    out = manifests / f"{exp_name}_handoff.json"
    out.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest

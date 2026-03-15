import json
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
REPORT_DIR = ROOT / "ingestion_reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _json_safe(obj):
    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, dict):
        return {k: _json_safe(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_json_safe(v) for v in obj]

    if isinstance(obj, tuple):
        return [_json_safe(v) for v in obj]

    return obj


def write_install_report(bundle_name: str, report: dict):
    safe_report = _json_safe(report)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_file = REPORT_DIR / f"{bundle_name}_{ts}.json"

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(safe_report, f, indent=2)

    return report_file

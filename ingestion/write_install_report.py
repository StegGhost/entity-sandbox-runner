import json
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
REPORT_DIR = ROOT / "ingestion_reports"
REPORT_DIR.mkdir(exist_ok=True)


def _normalize(obj):
    """
    Convert non-JSON types into safe serializable forms.
    """

    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, dict):
        return {k: _normalize(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [_normalize(v) for v in obj]

    if isinstance(obj, tuple):
        return [_normalize(v) for v in obj]

    return obj


def write_install_report(bundle_name: str, report: dict):

    report = _normalize(report)

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    report_file = REPORT_DIR / f"{bundle_name}_{ts}.json"

    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report_file

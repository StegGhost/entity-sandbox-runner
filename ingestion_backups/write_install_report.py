from pathlib import Path
from datetime import datetime, timezone
import json

def write_install_report(bundle_name: str, report: dict) -> str:
    reports = Path("ingestion_reports")
    reports.mkdir(parents=True, exist_ok=True)

    payload = {
        "bundle_name": bundle_name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        **report,
    }

    out = reports / f"{Path(bundle_name).stem}_install_report.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return str(out)

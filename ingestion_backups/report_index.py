from pathlib import Path
import json

def build_indexes() -> dict:
    report_root = Path("reports")
    data_root = Path("data_records")
    reports = [str(p) for p in sorted(report_root.rglob("*")) if p.is_file()]
    records = [str(p) for p in sorted(data_root.rglob("*")) if p.is_file()]

    report_index = {"report_count": len(reports), "reports": reports}
    record_index = {"record_count": len(records), "records": records}

    (report_root / "index.json").write_text(json.dumps(report_index, indent=2), encoding="utf-8")
    (data_root / "indexes").mkdir(parents=True, exist_ok=True)
    (data_root / "indexes" / "record_index.json").write_text(json.dumps(record_index, indent=2), encoding="utf-8")
    return {"reports": report_index, "records": record_index}

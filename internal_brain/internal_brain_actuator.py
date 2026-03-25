from pathlib import Path
import shutil
import json
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_read_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _match_report_for_bundle(report_dir: Path, bundle_name: str):
    candidates = sorted(
        [p for p in report_dir.glob("*.json") if bundle_name in p.name],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        return None

    report_path = candidates[0]
    report_json = _safe_read_json(report_path)

    return {
        "report_path": str(report_path),
        "report_relpath": str(report_path),
        "report_json": report_json,
    }


def actuate(closure_output, state):
    results = []
    root = Path(state["root"])

    failed_dir = root / "failed_bundles"
    incoming_dir = root / "incoming_bundles"
    report_dir = root / "ingestion_reports"
    feedback_dir = root / "payload" / "feedback"

    incoming_dir.mkdir(parents=True, exist_ok=True)
    feedback_dir.mkdir(parents=True, exist_ok=True)

    for action in closure_output.get("actions", []):
        name = action.get("action")
        targets = action.get("targets", [])

        if name == "inspect_failed_bundles":
            processed = []

            for rel_path in targets:
                src = root / rel_path
                if not src.exists() or not src.is_file():
                    continue

                dest = incoming_dir / src.name
                shutil.copy2(src, dest)
                processed.append(str(dest.relative_to(root)))

            results.append({
                "action": name,
                "status": "executed",
                "moved_to_incoming": processed,
                "count": len(processed),
                "ts": utc_now(),
            })

        elif name == "correlate_failed_bundles_with_ingestion_reports":
            correlations = []

            failed_bundles = sorted(
                [p for p in failed_dir.glob("*.zip") if p.is_file()],
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )[:20]

            for bundle_path in failed_bundles:
                match = _match_report_for_bundle(report_dir, bundle_path.name)
                entry = {
                    "bundle": str(bundle_path.relative_to(root)),
                    "bundle_name": bundle_path.name,
                    "matched_report": None,
                    "status": "no_report_found",
                }

                if match:
                    entry["matched_report"] = str(Path(match["report_path"]).relative_to(root))
                    entry["status"] = "matched"

                    report_json = match.get("report_json") or {}
                    verification = report_json.get("verification", {})
                    if verification:
                        entry["verification_reason"] = verification.get("reason")
                        entry["missing_fields"] = verification.get("missing_fields", [])
                        entry["allowed_paths"] = verification.get("manifest", {}).get("allowed_paths", [])

                correlations.append(entry)

            output_path = feedback_dir / "failed_bundle_report_correlation.json"
            with output_path.open("w", encoding="utf-8") as f:
                json.dump(
                    {
                        "ts": utc_now(),
                        "action": name,
                        "count": len(correlations),
                        "correlations": correlations,
                    },
                    f,
                    indent=2,
                )

            results.append({
                "action": name,
                "status": "executed",
                "output_file": str(output_path.relative_to(root)),
                "count": len(correlations),
                "matched": len([c for c in correlations if c["status"] == "matched"]),
                "unmatched": len([c for c in correlations if c["status"] != "matched"]),
                "ts": utc_now(),
            })

        else:
            results.append({
                "action": name,
                "status": "unknown_action",
                "targets": targets,
                "ts": utc_now(),
            })

    return {
        "mode": "active",
        "summary": "Actuator executed actions",
        "results": results,
    }

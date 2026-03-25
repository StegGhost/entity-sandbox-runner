from pathlib import Path
import shutil
import json
import zipfile
import tempfile
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


def _default_install_mode() -> str:
    return "folder_map"


def _default_allowed_paths_from_zip(extract_root: Path):
    allowed = []

    for path in sorted(extract_root.rglob("*")):
        if not path.is_file():
            continue

        rel = path.relative_to(extract_root).as_posix()
        if rel == "bundle_manifest.json":
            allowed.append("bundle_manifest.json")
            continue

        top = rel.split("/", 1)[0]
        if top in {"install", "payload", "experiments", "workflow_review", "config", "ui"}:
            prefix = f"{top}/"
            if prefix not in allowed:
                allowed.append(prefix)

    if "bundle_manifest.json" not in allowed:
        allowed.insert(0, "bundle_manifest.json")

    return allowed


def _repair_manifest(bundle_path: Path, target_info: dict, incoming_dir: Path):
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_root = Path(tmpdir)
        extract_root = tmp_root / "bundle"
        extract_root.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(bundle_path, "r") as zf:
            zf.extractall(extract_root)

        manifest_path = extract_root / "bundle_manifest.json"
        manifest = {}

        if manifest_path.exists():
            manifest = _safe_read_json(manifest_path) or {}

        if not manifest:
            manifest = {
                "bundle_name": bundle_path.stem,
                "bundle_version": "1.0.0",
            }

        missing_fields = target_info.get("missing_fields", [])
        existing_allowed = manifest.get("allowed_paths") or []
        suggested_allowed = target_info.get("allowed_paths") or []

        if "version" in missing_fields and "version" not in manifest:
            manifest["version"] = "1.0"

        if "install_mode" in missing_fields and "install_mode" not in manifest:
            manifest["install_mode"] = _default_install_mode()

        if "allowed_paths" in missing_fields and not manifest.get("allowed_paths"):
            manifest["allowed_paths"] = suggested_allowed or _default_allowed_paths_from_zip(extract_root)

        if not manifest.get("allowed_paths"):
            manifest["allowed_paths"] = existing_allowed or suggested_allowed or _default_allowed_paths_from_zip(extract_root)

        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

        repaired_name = bundle_path.stem + "_manifest_fixed.zip"
        repaired_zip = incoming_dir / repaired_name

        with zipfile.ZipFile(repaired_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for p in sorted(extract_root.rglob("*")):
                if p.is_file():
                    zf.write(p, p.relative_to(extract_root).as_posix())

        return repaired_zip, manifest


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

        elif name == "repair_bundle_manifests":
            repaired = []
            skipped = []

            for target in targets:
                bundle_rel = target.get("bundle")
                if not bundle_rel:
                    skipped.append({"target": target, "reason": "missing_bundle_path"})
                    continue

                bundle_path = root / bundle_rel
                if not bundle_path.exists():
                    skipped.append({"target": target, "reason": "bundle_not_found"})
                    continue

                repaired_zip, manifest = _repair_manifest(bundle_path, target, incoming_dir)
                repaired.append({
                    "source_bundle": bundle_rel,
                    "repaired_bundle": str(repaired_zip.relative_to(root)),
                    "missing_fields": target.get("missing_fields", []),
                    "reason": target.get("reason"),
                    "manifest_after_repair": manifest,
                })

            results.append({
                "action": name,
                "status": "executed",
                "repaired": repaired,
                "repaired_count": len(repaired),
                "skipped": skipped,
                "skipped_count": len(skipped),
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

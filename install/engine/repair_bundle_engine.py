import json
import os
import shutil
import tempfile
import zipfile
from datetime import datetime
from typing import Any, Dict, List, Tuple

ROOT = os.getcwd()
OUTPUT_DIR = os.path.join(ROOT, "incoming_bundles")
REPORT_PATH = os.path.join(ROOT, "brain_reports", "repair_report.json")

ALLOWED_PREFIXES = [
    "bundle_manifest.json",
    "install/",
    "install/engine/",
    "install/tests/",
]


def utc_now() -> str:
    return datetime.utcnow().isoformat()


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def write_json(path: str, payload: Dict[str, Any]) -> None:
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")


def is_allowed(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/")
    return any(
        normalized == prefix or normalized.startswith(prefix)
        for prefix in ALLOWED_PREFIXES
    )


def collect_zip_members(zip_path: str) -> List[str]:
    with zipfile.ZipFile(zip_path, "r") as zf:
        members = []
        for info in zf.infolist():
            if info.is_dir():
                continue
            members.append(info.filename.replace("\\", "/"))
        return members


def filter_members(members: List[str]) -> Tuple[List[str], List[str]]:
    allowed: List[str] = []
    filtered_out: List[str] = []

    for member in members:
        if is_allowed(member):
            allowed.append(member)
        else:
            filtered_out.append(member)

    return allowed, filtered_out


def build_repaired_bundle(source_zip: str, allowed_members: List[str], output_zip: str) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        extract_root = os.path.join(tmpdir, "bundle")
        os.makedirs(extract_root, exist_ok=True)

        with zipfile.ZipFile(source_zip, "r") as zf:
            zf.extractall(extract_root)

        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as out:
            for rel_path in allowed_members:
                full_path = os.path.join(extract_root, rel_path)
                if os.path.exists(full_path) and os.path.isfile(full_path):
                    out.write(full_path, rel_path)


def propose_repair(action_payload: Dict[str, Any]) -> Dict[str, Any]:
    target = action_payload.get("target")
    family = action_payload.get("family")
    reason = action_payload.get("reason")

    if not target:
        report = {
            "status": "failed",
            "reason": "no_target_bundle",
            "ts": utc_now(),
        }
        write_json(REPORT_PATH, report)
        return report

    source_zip = os.path.join(ROOT, target)
    if not os.path.exists(source_zip):
        report = {
            "status": "failed",
            "reason": "bundle_not_found",
            "target": target,
            "ts": utc_now(),
        }
        write_json(REPORT_PATH, report)
        return report

    ensure_dir(OUTPUT_DIR)

    try:
        original_members = collect_zip_members(source_zip)
        allowed_members, filtered_out = filter_members(original_members)

        if not allowed_members:
            report = {
                "status": "failed",
                "reason": "no_allowed_files_after_filtering",
                "target": target,
                "family": family,
                "filtered_out": filtered_out,
                "ts": utc_now(),
            }
            write_json(REPORT_PATH, report)
            return report

        source_name = os.path.basename(source_zip)
        if source_name.endswith(".zip"):
            repaired_name = source_name[:-4] + "_repaired.zip"
        else:
            repaired_name = source_name + "_repaired.zip"

        repaired_zip = os.path.join(OUTPUT_DIR, repaired_name)
        build_repaired_bundle(source_zip, allowed_members, repaired_zip)

        report = {
            "status": "ok",
            "action": "repair_generated",
            "original_bundle": target,
            "repaired_bundle": os.path.relpath(repaired_zip, ROOT).replace("\\", "/"),
            "family": family,
            "reason": reason,
            "original_file_count": len(original_members),
            "kept_file_count": len(allowed_members),
            "filtered_out_count": len(filtered_out),
            "filtered_out": filtered_out,
            "kept_files": allowed_members,
            "ts": utc_now(),
        }
        write_json(REPORT_PATH, report)
        return report

    except Exception as e:
        report = {
            "status": "failed",
            "reason": "repair_exception",
            "error": str(e),
            "target": target,
            "family": family,
            "ts": utc_now(),
        }
        write_json(REPORT_PATH, report)
        return report

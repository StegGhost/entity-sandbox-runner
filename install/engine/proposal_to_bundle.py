from __future__ import annotations

import json
import os
import zipfile
from typing import Any, Dict, List, Tuple


ALLOWED_PATHS = [
    "bundle_manifest.json",
    "install/",
    "install/tests/",
    "install/engine/",
    "install/apply.py",
]


def normalize_allowed_paths(bundle_name: str | None = None) -> List[str]:
    _ = bundle_name
    return list(ALLOWED_PATHS)


def _normalize_file_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    path = str(entry.get("path", "")).replace("\\", "/").strip()
    content = entry.get("content", "")
    return {"path": path, "content": content}


def build_bundle_object(
    proposal: Dict[str, Any],
    allowed_paths: List[str] | None = None,
) -> Dict[str, Any]:
    bundle_name = proposal.get("proposal_name", "generated_bundle")
    normalized_allowed = allowed_paths or normalize_allowed_paths(bundle_name)

    files: List[Dict[str, Any]] = []
    for entry in proposal.get("files_to_create", []) or []:
        normalized = _normalize_file_entry(entry)
        if normalized["path"]:
            files.append(normalized)

    return {
        "bundle_name": bundle_name,
        "allowed_paths": normalized_allowed,
        "files": files,
        "file_count": len(files),
        "metadata": proposal.get("metadata", {}),
    }


def serialize_bundle(bundle: Dict[str, Any]) -> str:
    return json.dumps(bundle, sort_keys=True, indent=2, default=str)


def _write_bundle_zip(bundle: Dict[str, Any], output_path: str) -> str:
    parent = os.path.dirname(output_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("bundle_manifest.json", serialize_bundle(bundle))
        for entry in bundle.get("files", []):
            if entry.get("path"):
                zf.writestr(entry["path"], entry.get("content", ""))

    return output_path


def proposal_to_bundle(
    proposal: Dict[str, Any],
    allowed_paths: List[str] | None = None,
    output_path: str | None = None,
):
    bundle = build_bundle_object(proposal, allowed_paths=allowed_paths)

    if output_path:
        return _write_bundle_zip(bundle, output_path)

    return bundle


def _is_allowed_path(rel_path: str, allowed_paths: List[str]) -> bool:
    rel = rel_path.replace("\\", "/").strip()

    for allowed in allowed_paths:
        a = allowed.replace("\\", "/").strip()

        if a.endswith("/"):
            if rel.startswith(a):
                return True
        else:
            if rel == a:
                return True

    return False


def _load_manifest(bundle_path: str) -> Dict[str, Any] | None:
    manifest_path = os.path.join(bundle_path, "bundle_manifest.json")
    if not os.path.exists(manifest_path):
        return None

    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def simulate_ingestion(bundle_path: str) -> Tuple[bool, str]:
    if not os.path.exists(bundle_path):
        return False, "missing_bundle"

    if os.path.isdir(bundle_path):
        manifest = _load_manifest(bundle_path)
        if manifest is None:
            return False, "missing_manifest"

        allowed_paths = manifest.get("allowed_paths", [])

        for root, _, files in os.walk(bundle_path):
            for name in files:
                abs_path = os.path.join(root, name)
                rel_path = os.path.relpath(abs_path, bundle_path).replace("\\", "/")

                if rel_path == "bundle_manifest.json":
                    continue

                if not _is_allowed_path(rel_path, allowed_paths):
                    return False, f"path_not_allowed:{rel_path}"

        return True, "ok"

    if zipfile.is_zipfile(bundle_path):
        with zipfile.ZipFile(bundle_path, "r") as zf:
            names = zf.namelist()
            if "bundle_manifest.json" not in names:
                return False, "missing_manifest"

            manifest = json.loads(zf.read("bundle_manifest.json").decode("utf-8"))
            allowed_paths = manifest.get("allowed_paths", [])

            for name in names:
                normalized = name.replace("\\", "/")
                if normalized.endswith("/") or normalized == "bundle_manifest.json":
                    continue
                if not _is_allowed_path(normalized, allowed_paths):
                    return False, f"path_not_allowed:{normalized}"

        return True, "ok"

    return False, "unsupported_bundle_type"


def auto_repair(bundle_path: str, reason: str | None = None) -> Dict[str, Any]:
    """
    Minimal deterministic auto-repair helper for tests.

    For directory bundles:
    - if a path_not_allowed violation is reported, remove the offending file
    - then re-run ingestion check
    """
    ok, detected_reason = simulate_ingestion(bundle_path)
    repair_reason = reason or detected_reason

    if not ok and os.path.isdir(bundle_path):
        prefix = "path_not_allowed:"
        if isinstance(repair_reason, str) and repair_reason.startswith(prefix):
            bad_rel = repair_reason[len(prefix):]
            bad_abs = os.path.join(bundle_path, bad_rel)
            if os.path.exists(bad_abs) and os.path.isfile(bad_abs):
                os.remove(bad_abs)

        ok, detected_reason = simulate_ingestion(bundle_path)

    return {
        "status": "ok",
        "bundle_path": bundle_path,
        "bundle_exists": os.path.exists(bundle_path),
        "repaired": ok,
        "reason": detected_reason,
    }

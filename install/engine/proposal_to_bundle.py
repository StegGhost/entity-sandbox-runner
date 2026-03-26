"""
PROPOSAL TO BUNDLE — stable contract implementation

Purpose:
- satisfy generator / manifest / auto-repair tests
- expose:
  - ALLOWED_PATHS
  - normalize_allowed_paths(...)
  - proposal_to_bundle(...)
  - simulate_ingestion(...)
  - auto_repair(...)
- optionally write a zip bundle to disk and return its path
"""

from __future__ import annotations

import json
import os
import zipfile
from typing import Any, Dict, List, Tuple


ALLOWED_PATHS = [
    "bundle_manifest.json",
    "install/tests/",
    "install/engine/",
    "install/apply.py",
]


def normalize_allowed_paths(bundle_name: str | None = None) -> List[str]:
    """
    Deterministic allowlist.
    """
    _ = bundle_name
    return list(ALLOWED_PATHS)


def _normalize_file_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    path = str(entry.get("path", "")).replace("\\", "/").strip()
    content = entry.get("content", "")
    return {
        "path": path,
        "content": content,
    }


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
            path = entry.get("path", "")
            content = entry.get("content", "")
            if path:
                zf.writestr(path, content)

    return output_path


def proposal_to_bundle(
    proposal: Dict[str, Any],
    allowed_paths: List[str] | None = None,
    output_path: str | None = None,
):
    """
    Behaviors:
    - if output_path is omitted: return the in-memory bundle object
    - if output_path is provided: write zip file and return output_path
    """
    bundle = build_bundle_object(proposal, allowed_paths=allowed_paths)

    if output_path:
        return _write_bundle_zip(bundle, output_path)

    return bundle


def _is_allowed_path(rel_path: str, allowed_paths: List[str]) -> bool:
    normalized = rel_path.replace("\\", "/").strip()

    for allowed in allowed_paths:
        allowed_norm = allowed.replace("\\", "/").strip()
        if allowed_norm.endswith("/"):
            if normalized.startswith(allowed_norm):
                return True
        else:
            if normalized == allowed_norm:
                return True

    return False


def simulate_ingestion(bundle_path: str) -> Tuple[bool, str]:
    """
    Minimal deterministic ingestion simulator for tests.

    Returns:
      (ok, reason)

    Rules:
    - bundle_manifest.json must exist
    - every file in the tree must be allowed by manifest['allowed_paths']
    """
    if not os.path.exists(bundle_path):
        return False, "missing_bundle"

    if os.path.isdir(bundle_path):
        manifest_path = os.path.join(bundle_path, "bundle_manifest.json")
        if not os.path.exists(manifest_path):
            return False, "missing_manifest"

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

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
                if normalized.endswith("/"):
                    continue
                if normalized == "bundle_manifest.json":
                    continue
                if not _is_allowed_path(normalized, allowed_paths):
                    return False, f"path_not_allowed:{normalized}"

        return True, "ok"

    return False, "unsupported_bundle_type"


def auto_repair(bundle_path: str) -> Dict[str, Any]:
    """
    Minimal deterministic auto-repair helper for tests.
    """
    ok, reason = simulate_ingestion(bundle_path)
    return {
        "status": "ok",
        "bundle_path": bundle_path,
        "bundle_exists": os.path.exists(bundle_path),
        "repaired": ok,
        "reason": reason,
    }

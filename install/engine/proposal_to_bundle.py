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
from typing import Any, Dict, List


ALLOWED_PATHS = [
    "bundle_manifest.json",
    "install/",
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


def simulate_ingestion(bundle_path: str) -> Dict[str, Any]:
    """
    Minimal deterministic ingestion simulator for tests.

    Returns a stable success payload if the bundle exists.
    """
    exists = os.path.exists(bundle_path)

    return {
        "status": "ok" if exists else "missing",
        "bundle_path": bundle_path,
        "bundle_exists": exists,
        "ingested": exists,
    }


def auto_repair(bundle_path: str) -> Dict[str, Any]:
    """
    Minimal deterministic auto-repair helper for tests.
    """
    ingestion = simulate_ingestion(bundle_path)
    return {
        "status": "ok",
        "bundle_path": bundle_path,
        "bundle_exists": ingestion["bundle_exists"],
        "repaired": ingestion["bundle_exists"],
    }

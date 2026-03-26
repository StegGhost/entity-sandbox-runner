"""
PROPOSAL TO BUNDLE — minimal stable contract implementation

Purpose:
- normalize allowed paths for generated bundle files
- convert proposal payloads into a deterministic bundle-like structure
- satisfy generator_v2 / self_improve contract imports
"""

from __future__ import annotations

import json
from typing import Any, Dict, List


def normalize_allowed_paths(paths: List[str]) -> List[str]:
    """
    Normalize path allowlists so callers have a stable contract.

    Rules:
    - convert backslashes to forward slashes
    - strip whitespace
    - remove empty entries
    - de-duplicate while preserving order
    - ensure directory-like allowed roots end with '/'
    """
    seen = set()
    normalized: List[str] = []

    for raw in paths or []:
        if raw is None:
            continue

        path = str(raw).replace("\\", "/").strip()
        if not path:
            continue

        if not path.endswith("/") and "." not in path.split("/")[-1]:
            path = path + "/"

        if path not in seen:
            seen.add(path)
            normalized.append(path)

    return normalized


def _normalize_file_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    path = str(entry.get("path", "")).replace("\\", "/").strip()
    content = entry.get("content", "")

    return {
        "path": path,
        "content": content,
    }


def proposal_to_bundle(proposal: Dict[str, Any], allowed_paths: List[str] | None = None) -> Dict[str, Any]:
    """
    Convert a proposal object into a deterministic bundle structure.
    """
    normalized_allowed = normalize_allowed_paths(allowed_paths or [])

    files = []
    for entry in proposal.get("files_to_create", []) or []:
        normalized = _normalize_file_entry(entry)
        if normalized["path"]:
            files.append(normalized)

    return {
        "bundle_name": proposal.get("proposal_name", "generated_bundle"),
        "allowed_paths": normalized_allowed,
        "files": files,
        "file_count": len(files),
        "metadata": proposal.get("metadata", {}),
    }


def serialize_bundle(bundle: Dict[str, Any]) -> str:
    """
    Deterministic JSON serialization helper.
    """
    return json.dumps(bundle, sort_keys=True, indent=2, default=str)

from pathlib import Path
import json


def _read_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _normalize_prefix(p: str) -> str:
    return str(Path(p)).replace("\\", "/").rstrip("/")


def _infer_allowed_paths(bundle_root: Path):
    """
    Dev-manifest fallback:
    infer top-level writable areas from bundle contents.

    Rules:
    - normal top-level folders become '<top>/'
    - workflow files are mapped to 'workflow_review/'
    - .git and anything with '..' is ignored
    """
    allowed = set()

    for item in bundle_root.rglob("*"):
        if item.is_dir():
            continue

        rel = item.relative_to(bundle_root)
        rel_str = str(rel).replace("\\", "/")

        if not rel_str or ".." in rel.parts:
            continue

        if rel_str.startswith(".github/workflows/"):
            allowed.add("workflow_review/")
            continue

        top = rel.parts[0]
        if top in {".git", ".github"}:
            continue

        allowed.add(f"{top}/")

    return sorted(allowed)


def _generate_dev_manifest(bundle_root: Path):
    manifest_candidates = []
    for p in bundle_root.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(bundle_root)).replace("\\", "/")
            manifest_candidates.append(rel)

    bundle_name = bundle_root.name
    allowed_paths = _infer_allowed_paths(bundle_root)

    return {
        "bundle_name": bundle_name,
        "version": "dev",
        "install_mode": "folder_map",
        "dev_bundle": True,
        "generated_manifest": True,
        "allowed_paths": allowed_paths,
        "files": manifest_candidates,
    }


def _validate_required_fields(manifest: dict):
    required = ["bundle_name", "version", "install_mode", "allowed_paths"]

    missing = [k for k in required if k not in manifest]
    if missing:
        return {
            "verified": False,
            "reason": "manifest_missing_required_fields",
            "missing_fields": missing,
        }

    if not isinstance(manifest["allowed_paths"], list) or not manifest["allowed_paths"]:
        return {
            "verified": False,
            "reason": "allowed_paths_required",
            "missing_fields": [],
        }

    normalized = []
    for p in manifest["allowed_paths"]:
        p_norm = _normalize_prefix(p)
        if p_norm:
            normalized.append(p_norm + "/" if not p_norm.endswith("/") else p_norm)

    manifest["allowed_paths"] = normalized

    return {
        "verified": True,
        "reason": "manifest_schema_valid",
    }


def enforce_manifest(bundle_root: Path):
    """
    Returns a dict with:
    - manifest_found
    - verified
    - reason
    - manifest
    - manifest_path (when present)
    """

    manifest_candidates = [
        bundle_root / "bundle_manifest.json",
        bundle_root / "bundle_manifest_standard.json",
    ]

    manifest_path = None
    for candidate in manifest_candidates:
        if candidate.exists():
            manifest_path = candidate
            break

    # Dev fallback mode
    if manifest_path is None:
        manifest = _generate_dev_manifest(bundle_root)

        schema_result = _validate_required_fields(manifest)
        if not schema_result["verified"]:
            return {
                "manifest_found": False,
                "verified": False,
                "reason": schema_result["reason"],
                "missing_fields": schema_result.get("missing_fields", []),
                "manifest": manifest,
            }

        return {
            "manifest_found": False,
            "verified": True,
            "reason": "generated_dev_manifest",
            "manifest": manifest,
        }

    # Normal manifest mode
    try:
        manifest = _read_json(manifest_path)
    except Exception as e:
        return {
            "manifest_found": True,
            "verified": False,
            "reason": "manifest_parse_failed",
            "error": repr(e),
            "manifest_path": str(manifest_path),
        }

    schema_result = _validate_required_fields(manifest)
    if not schema_result["verified"]:
        return {
            "manifest_found": True,
            "verified": False,
            "reason": schema_result["reason"],
            "missing_fields": schema_result.get("missing_fields", []),
            "manifest_path": str(manifest_path),
            "manifest": manifest,
        }

    return {
        "manifest_found": True,
        "verified": True,
        "reason": "manifest_valid",
        "manifest_path": str(manifest_path),
        "manifest": manifest,
    }

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _is_allowed(path_str, allowed):
    for a in allowed:
        if a.endswith("/"):
            if path_str.startswith(a):
                return True
        else:
            if path_str == a:
                return True
    return False


def validate_capabilities(bundle_dir, manifest):
    allowed = manifest.get("allowed_paths", [])

    violations = []
    normal_files = []
    workflow_files = []

    for p in bundle_dir.rglob("*"):
        if not p.is_file():
            continue

        rel = p.relative_to(bundle_dir)
        path_str = rel.as_posix()

        if not _is_allowed(path_str, allowed):
            violations.append(path_str)
        else:
            normal_files.append(path_str)
            if ".github/workflows/" in path_str:
                workflow_files.append(path_str)

    return {
        "verified": len(violations) == 0,
        "allowed_paths": allowed,
        "violations": violations,
        "filtered_normal_files": normal_files,
        "filtered_workflow_files": workflow_files
    }

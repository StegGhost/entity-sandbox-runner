import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def validate_capabilities(bundle_dir, manifest):

    allowed = manifest.get("allowed_paths", [])

    violations = []
    normal_files = []
    workflow_files = []

    for p in bundle_dir.rglob("*"):

        if not p.is_file():
            continue

        rel = p.relative_to(bundle_dir)

        path_str = str(rel)

        allowed_match = False

        for a in allowed:

            if path_str.startswith(a):
                allowed_match = True
                break

        if not allowed_match:
            violations.append(path_str)
        else:
            normal_files.append(path_str)

            if ".github/workflows" in path_str:
                workflow_files.append(path_str)

    return {
        "verified": len(violations) == 0,
        "allowed_paths": allowed,
        "violations": violations,
        "filtered_normal_files": normal_files,
        "filtered_workflow_files": workflow_files
    }

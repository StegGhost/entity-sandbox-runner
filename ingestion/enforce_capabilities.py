from pathlib import Path


def _normalize(rel_path: str) -> str:
    return str(Path(rel_path)).replace("\\", "/").rstrip("/")


def _matches_allowed(rel_path: str, allowed_paths: list[str]) -> bool:
    rel_path = _normalize(rel_path)

    for allowed in allowed_paths:
        allowed = _normalize(allowed)

        if not allowed:
            continue

        if rel_path == allowed:
            return True

        if rel_path.startswith(allowed + "/"):
            return True

    return False


def _classify_declared_target(rel_str: str) -> str:
    if rel_str.startswith(".github/workflows/"):
        return "workflow_review"
    return rel_str


def enforce_capabilities(manifest: dict, normal_files, workflow_files):
    allowed_paths = manifest.get("allowed_paths", [])

    if not allowed_paths:
        return {
            "verified": False,
            "reason": "allowed_paths_required",
            "violations": [str(p) for p in normal_files] + [str(p) for p in workflow_files],
            "filtered_normal_files": [],
            "filtered_workflow_files": [],
        }

    violations = []
    filtered_normal_files = []
    filtered_workflow_files = []

    for rel in normal_files:
        rel_str = str(rel).replace("\\", "/")
        declared_target = _classify_declared_target(rel_str)

        if _matches_allowed(declared_target, allowed_paths):
            filtered_normal_files.append(rel)
        else:
            violations.append(rel_str)

    for rel in workflow_files:
        rel_str = str(rel).replace("\\", "/")
        declared_target = "workflow_review/" + Path(rel_str).name

        if (
            _matches_allowed("workflow_review", allowed_paths)
            or _matches_allowed(declared_target, allowed_paths)
        ):
            filtered_workflow_files.append(rel)
        else:
            violations.append(rel_str)

    return {
        "verified": len(violations) == 0,
        "reason": "capabilities_enforced" if len(violations) == 0 else "capability_violation",
        "allowed_paths": allowed_paths,
        "violations": violations,
        "filtered_normal_files": filtered_normal_files,
        "filtered_workflow_files": filtered_workflow_files,
    }

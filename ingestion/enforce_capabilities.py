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


def enforce_capabilities(manifest: dict, normal_files, workflow_files):
    allowed_paths = manifest.get("allowed_paths", [])

    # If no allowed_paths are declared, fail closed.
    if not allowed_paths:
        return {
            "verified": False,
            "reason": "allowed_paths_required",
            "violations": [str(p) for p in normal_files] + [str(p) for p in workflow_files],
        }

    violations = []

    for rel in normal_files:
        rel_str = str(rel).replace("\\", "/")
        if not _matches_allowed(rel_str, allowed_paths):
            violations.append(rel_str)

    # Workflows are staged into workflow_review/, so require the bundle to declare
    # permission to affect workflow material explicitly.
    if workflow_files:
        workflow_cap_ok = (
            "workflow_review" in [p.rstrip("/") for p in allowed_paths]
            or "workflow_review/" in allowed_paths
        )

        if not workflow_cap_ok:
            for rel in workflow_files:
                violations.append(str(rel).replace("\\", "/"))

    return {
        "verified": len(violations) == 0,
        "reason": "capabilities_enforced" if len(violations) == 0 else "capability_violation",
        "allowed_paths": allowed_paths,
        "violations": violations,
    }

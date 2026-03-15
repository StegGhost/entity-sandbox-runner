from pathlib import Path

ALLOWED_TOP_LEVEL = {
    "adaptive_scanner",
    "data_records",
    "entities",
    "experiments",
    "failed_bundles",
    "ingestion",
    "ingestion_backups",
    "ingestion_reports",
    "installed_bundles",
    "interaction_graph",
    "manifests",
    "observatory",
    "receipts",
    "reports",
    "reproducibility",
    "results",
    "runner",
    "sandbox",
    "sdk",
    "statistics",
    "visualization",
    "workflow_review",
}

BLOCKED_TOP_LEVEL = {
    ".git",
    ".github",
}

def validate_relative_path(rel: Path):
    rel_str = str(rel).replace("\\", "/")

    if not rel_str or rel_str == ".":
        raise ValueError("empty relative path")

    if rel.is_absolute():
        raise ValueError(f"absolute path not allowed: {rel_str}")

    if ".." in rel.parts:
        raise ValueError(f"path traversal not allowed: {rel_str}")

    top = rel.parts[0]
    if top in BLOCKED_TOP_LEVEL:
        raise ValueError(f"protected top-level path blocked: {rel_str}")

    if top not in ALLOWED_TOP_LEVEL:
        raise ValueError(f"top-level path not allowed: {rel_str}")

    return rel

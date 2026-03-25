import os
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent.parent.parent
BRAIN_REPORTS = ROOT / "brain_reports"

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
    "_workspace",
    "ingestion_tmp",
    "_ingest_tmp",
    ".idea",
    ".vscode",
}

MAX_ENTRIES_PER_SECTION = 200
MAX_DEPTH = 4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def safe_iterdir(path: Path):
    try:
        return sorted(
            [p for p in path.iterdir() if not should_ignore(p)],
            key=lambda p: (p.is_file(), p.name.lower()),
        )
    except Exception:
        return []


def walk_tree(root: Path, max_depth: int = MAX_DEPTH) -> list[str]:
    lines: list[str] = []

    def recurse(path: Path, prefix: str = "", depth: int = 0):
        if depth >= max_depth:
            return

        children = safe_iterdir(path)
        if len(children) > MAX_ENTRIES_PER_SECTION:
            children = children[:MAX_ENTRIES_PER_SECTION]

        for idx, child in enumerate(children):
            connector = "└── " if idx == len(children) - 1 else "├── "
            suffix = "/" if child.is_dir() else ""
            lines.append(f"{prefix}{connector}{child.name}{suffix}")
            if child.is_dir():
                extension = "    " if idx == len(children) - 1 else "│   "
                recurse(child, prefix + extension, depth + 1)

    lines.append(f"{root.name}/")
    recurse(root)
    return lines


def write_md(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"# {title}\n\nGenerated: {utc_now()}\n\n{body}"
    path.write_text(content, encoding="utf-8")


def markdown_tree(root: Path, max_depth: int = MAX_DEPTH) -> str:
    return "```text\n" + "\n".join(walk_tree(root, max_depth=max_depth)) + "\n```\n"


def list_dir_entries(path: Path) -> str:
    entries = safe_iterdir(path)
    if not entries:
        return "- empty\n"

    lines = []
    for entry in entries[:MAX_ENTRIES_PER_SECTION]:
        suffix = "/" if entry.is_dir() else ""
        lines.append(f"- {entry.name}{suffix}")
    return "\n".join(lines) + "\n"


def summarize_root() -> None:
    root_items = safe_iterdir(ROOT)
    body = "## Top-level entries\n\n"
    for item in root_items[:MAX_ENTRIES_PER_SECTION]:
        suffix = "/" if item.is_dir() else ""
        body += f"- {item.name}{suffix}\n"

    body += "\n## Compact root tree\n\n"
    body += markdown_tree(ROOT, max_depth=2)

    write_md(BRAIN_REPORTS / "repo_root_map.md", "Repo Root Map", body)


def summarize_install() -> None:
    install_dir = ROOT / "install"
    engine_dir = install_dir / "engine"

    body = "## install/\n\n"
    body += list_dir_entries(install_dir)
    body += "\n## install/ tree\n\n"
    body += markdown_tree(install_dir, max_depth=3)

    if engine_dir.exists():
        body += "\n## install/engine/\n\n"
        body += list_dir_entries(engine_dir)
        body += "\n## install/engine tree\n\n"
        body += markdown_tree(engine_dir, max_depth=2)

    write_md(BRAIN_REPORTS / "repo_install_map.md", "Install Surface Map", body)


def summarize_workflows() -> None:
    wf_dir = ROOT / ".github" / "workflows"
    body = "## .github/workflows/\n\n"
    body += list_dir_entries(wf_dir)
    body += "\n## Workflow tree\n\n"
    body += markdown_tree(wf_dir, max_depth=2)
    write_md(BRAIN_REPORTS / "repo_workflow_map.md", "Workflow Map", body)


def summarize_bundle_surfaces() -> None:
    incoming = ROOT / "incoming_bundles"
    installed = ROOT / "installed_bundles"
    failed = ROOT / "failed_bundles"

    body = "## incoming_bundles/\n\n"
    body += list_dir_entries(incoming)

    body += "\n## installed_bundles/\n\n"
    body += list_dir_entries(installed)

    body += "\n## failed_bundles/\n\n"
    body += list_dir_entries(failed)

    write_md(BRAIN_REPORTS / "repo_bundle_surfaces.md", "Bundle Surface Map", body)


def summarize_state_surfaces() -> None:
    body = ""

    for rel in ["brain_reports", "receipts", "logs", "payload", "ingestion_reports", "internal_brain"]:
        path = ROOT / rel
        body += f"## {rel}/\n\n"
        body += list_dir_entries(path)
        body += "\n"

    write_md(BRAIN_REPORTS / "repo_state_surfaces.md", "State Surface Map", body)


def summarize_architecture_snapshot() -> None:
    body = """## Current reading

- `internal_brain/` is the decision and reconciliation surface.
- `install/` is the execution/tooling surface and is currently overloaded.
- `incoming_bundles/`, `installed_bundles/`, and `failed_bundles/` are the operational bundle lifecycle.
- `brain_reports/`, `receipts/`, `logs/`, and `payload/` are the major evidence/state surfaces.
- `.github/workflows/` is the automation/control wiring surface.
- `payload/` appears to mirror or duplicate major architectural surfaces and should be treated as a distinct subsystem, not just a misc folder.

## Immediate operational concerns

- One giant repo tree is too large for iPhone inspection.
- `install/` has enough files that it needs its own map.
- Bundle lifecycle inspection should stay separate from root tree inspection.
- Workflow inspection should stay separate from state/evidence inspection.
- Temporary or staging roots like `_ingest_tmp/` should not drive architectural interpretation.

## Generated map set

- `repo_root_map.md`
- `repo_install_map.md`
- `repo_workflow_map.md`
- `repo_bundle_surfaces.md`
- `repo_state_surfaces.md`

These are the iPhone-friendly operational maps and should be used instead of one oversized tree dump.
"""
    write_md(BRAIN_REPORTS / "architecture_snapshot.md", "Architecture Snapshot", body)


def write_index() -> None:
    body = """## Available generated maps

- `repo_root_map.md` — top-level repo view
- `repo_install_map.md` — install and install/engine surface
- `repo_workflow_map.md` — workflow inventory
- `repo_bundle_surfaces.md` — incoming / installed / failed bundle surfaces
- `repo_state_surfaces.md` — brain_reports / receipts / logs / payload / ingestion_reports / internal_brain
- `architecture_snapshot.md` — operational reading of the repo

## Recommended usage

Start with:
1. `repo_root_map.md`
2. `repo_bundle_surfaces.md`
3. `repo_install_map.md`

Only open the others when narrowing a specific issue.
"""
    write_md(BRAIN_REPORTS / "repo_map_index.md", "Repo Map Index", body)


def main() -> int:
    BRAIN_REPORTS.mkdir(parents=True, exist_ok=True)

    summarize_root()
    summarize_install()
    summarize_workflows()
    summarize_bundle_surfaces()
    summarize_state_surfaces()
    summarize_architecture_snapshot()
    write_index()

    print(str(BRAIN_REPORTS / "repo_map_index.md"))
    print(str(BRAIN_REPORTS / "repo_root_map.md"))
    print(str(BRAIN_REPORTS / "repo_install_map.md"))
    print(str(BRAIN_REPORTS / "repo_workflow_map.md"))
    print(str(BRAIN_REPORTS / "repo_bundle_surfaces.md"))
    print(str(BRAIN_REPORTS / "repo_state_surfaces.md"))
    print(str(BRAIN_REPORTS / "architecture_snapshot.md"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

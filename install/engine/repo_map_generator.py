import os
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent.parent.parent
BRAIN_REPORTS = ROOT / "brain_reports"
TREE_PATH = BRAIN_REPORTS / "repo_file_tree.md"
ARCH_PATH = BRAIN_REPORTS / "architecture_snapshot.md"

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
    ".idea",
    ".vscode",
}

MAX_FILES_PER_DIR = 200


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def should_ignore(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)


def walk_tree(root: Path) -> list[str]:
    lines: list[str] = []

    def recurse(path: Path, prefix: str = ""):
        try:
            children = sorted(
                [p for p in path.iterdir() if not should_ignore(p)],
                key=lambda p: (p.is_file(), p.name.lower())
            )
        except Exception:
            return

        if len(children) > MAX_FILES_PER_DIR:
            children = children[:MAX_FILES_PER_DIR]

        for idx, child in enumerate(children):
            connector = "└── " if idx == len(children) - 1 else "├── "
            lines.append(f"{prefix}{connector}{child.name}")
            if child.is_dir():
                extension = "    " if idx == len(children) - 1 else "│   "
                recurse(child, prefix + extension)

    lines.append(f"{root.name}/")
    recurse(root)
    return lines


def list_top_level_dirs(root: Path) -> list[str]:
    items = []
    for p in sorted(root.iterdir(), key=lambda x: x.name.lower()):
        if should_ignore(p):
            continue
        if p.is_dir():
            items.append(f"- {p.name}/")
        else:
            items.append(f"- {p.name}")
    return items


def summarize_operational_surfaces(root: Path) -> str:
    sections = []

    key_dirs = [
        "internal_brain",
        "install",
        "incoming_bundles",
        "installed_bundles",
        "failed_bundles",
        "receipts",
        "logs",
        "payload",
        "brain_reports",
        ".github/workflows",
    ]

    for rel in key_dirs:
        path = root / rel
        if not path.exists():
            continue

        sections.append(f"## {rel}\n")

        if path.is_file():
            sections.append(f"- file: {rel}\n")
            continue

        try:
            entries = sorted(
                [p.name + ("/" if (path / p.name).is_dir() else "") for p in path.iterdir() if not should_ignore(path / p.name)],
                key=lambda x: x.lower()
            )
        except Exception:
            entries = []

        if not entries:
            sections.append("- empty\n")
        else:
            for entry in entries[:100]:
                sections.append(f"- {entry}\n")

        sections.append("\n")

    return "".join(sections)


def write_repo_tree(root: Path) -> None:
    lines = walk_tree(root)
    content = [
        f"# Repo File Tree\n",
        f"Generated: {utc_now()}\n",
        "```text",
        *lines,
        "```",
        "",
    ]
    TREE_PATH.write_text("\n".join(content), encoding="utf-8")


def write_architecture_snapshot(root: Path) -> None:
    top_level = list_top_level_dirs(root)
    operational = summarize_operational_surfaces(root)

    content = f"""# Architecture Snapshot

Generated: {utc_now()}

## Current root surface

{chr(10).join(top_level)}

## Operational interpretation

{operational}## Architectural reading

- `internal_brain/` is the decision and reconciliation surface.
- `install/` contains execution-side tooling and ingestion/runtime engines.
- `incoming_bundles/` is the bundle ingress queue.
- `installed_bundles/` is the admitted bundle surface.
- `failed_bundles/` is the rejected or unresolved bundle surface.
- `receipts/`, `logs/`, `payload/`, and `brain_reports/` are the current evidence/state surfaces.
- `.github/workflows/` is the automation/control wiring surface.

## Immediate use

This file is a generated operational snapshot for fast human inspection from iPhone.
It is not the canonical architecture paper or design doc.
"""
    ARCH_PATH.write_text(content, encoding="utf-8")


def main() -> int:
    BRAIN_REPORTS.mkdir(parents=True, exist_ok=True)
    write_repo_tree(ROOT)
    write_architecture_snapshot(ROOT)
    print(str(TREE_PATH))
    print(str(ARCH_PATH))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

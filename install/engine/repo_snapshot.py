import hashlib
import json
import os
import time
from pathlib import Path


TRACE_LOG_PATH = Path("brain_reports/repo_snapshot_trace.jsonl")
DEFAULT_OUTPUT_PATH = Path("payload/runtime/repo_snapshot.json")


def _safe_read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _safe_read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _scan_bundle_dir(path: Path):
    if not path.exists() or not path.is_dir():
        return []
    return sorted([p.name for p in path.iterdir() if p.is_file() and p.name.endswith(".zip")])


def _find_cge_bundle_state(root: Path):
    incoming = _scan_bundle_dir(root / "incoming_bundles")
    installed = _scan_bundle_dir(root / "installed_bundles")
    failed = _scan_bundle_dir(root / "failed_bundles")

    def _filter_cge(items):
        return [name for name in items if "cge" in name.lower()]

    incoming_cge = _filter_cge(incoming)
    installed_cge = _filter_cge(installed)
    failed_cge = _filter_cge(failed)

    has_cge = bool(incoming_cge or installed_cge or failed_cge)

    if installed_cge:
        cge_state = "installed"
    elif incoming_cge:
        cge_state = "pending"
    elif failed_cge:
        cge_state = "failed"
    else:
        cge_state = "absent"

    return {
        "has_cge": has_cge,
        "cge_state": cge_state,
        "incoming_cge_bundles": incoming_cge,
        "installed_cge_bundles": installed_cge,
        "failed_cge_bundles": failed_cge,
        "incoming_bundle_count": len(incoming),
        "installed_bundle_count": len(installed),
        "failed_bundle_count": len(failed),
    }


def _collect_files(root: Path):
    files = []
    tests = []

    excluded_dirs = {
        ".git",
        ".github",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".venv",
        "venv",
        "ingestion_backups",
        "experiments",
    }

    for p in root.rglob("*"):
        if not p.is_file():
            continue

        rel = str(p.relative_to(root)).replace("\\", "/")
        parts = set(rel.split("/"))
        if parts & excluded_dirs:
            continue

        files.append(rel)

        name = p.name
        if name.startswith("test_") or "/tests/" in f"/{rel}/":
            tests.append(rel)

    files.sort()
    tests.sort()
    return files, tests


def _hash_paths_and_contents(root: Path, rel_paths):
    material = []
    for rel in rel_paths:
        p = root / rel
        material.append({
            "path": rel,
            "content_hash": _sha256_text(_safe_read_text(p)),
        })
    return _sha256_text(json.dumps(material, sort_keys=True, separators=(",", ":")))


def _trace_snapshot(snapshot: dict):
    if os.getenv("REPO_SNAPSHOT_TRACE", "1") != "1":
        return

    TRACE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": time.time(),
        "module_name": __name__,
        "module_file": __file__,
        "cwd": os.getcwd(),
        "root": snapshot.get("root"),
        "repo_hash": snapshot.get("repo_hash"),
        "test_surface_hash": snapshot.get("test_surface_hash"),
        "has_cge": snapshot.get("has_cge"),
        "cge_state": snapshot.get("cge_state"),
        "incoming_bundle_count": snapshot.get("incoming_bundle_count"),
        "installed_bundle_count": snapshot.get("installed_bundle_count"),
        "failed_bundle_count": snapshot.get("failed_bundle_count"),
    }

    with TRACE_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def build_snapshot(root="."):
    root = Path(root)
    files, tests = _collect_files(root)

    buildout_registry = _safe_read_json(root / ".buildout_registry.json") or {}
    phase_registry = _safe_read_json(root / ".buildout_phase_registry.json") or {}
    reconciled = _safe_read_json(root / "brain_reports" / "reconciled_state.json") or {}
    execution = _safe_read_json(root / "brain_reports" / "execute_next_action_result.json") or {}
    next_action = _safe_read_json(root / "brain_reports" / "next_action.json") or {}

    cge_info = _find_cge_bundle_state(root)

    snapshot = {
        "generated_at": time.time(),
        "root": str(root),
        "file_count": len(files),
        "test_count": len(tests),
        "files": files[:200],
        "tests": tests[:200],
        "registry_entry_count": len(buildout_registry),
        "phase_registry_entry_count": len(phase_registry),
        "latest_global_root": None,
        "has_pending_bundles": cge_info["incoming_bundle_count"] > 0,
        "snapshot_source_module": __name__,
        "snapshot_source_file": __file__,
        "repo_hash": _hash_paths_and_contents(root, files),
        "test_surface_hash": _hash_paths_and_contents(root, tests),
        "last_review_state": (reconciled.get("review") or {}).get("state"),
        "last_execution_status": (execution.get("execution") or {}).get("status"),
        "last_next_action": (next_action.get("next_action") or {}).get("action"),
        **cge_info,
    }

    _trace_snapshot(snapshot)
    return snapshot


def snapshot_repo_state(root="."):
    return build_snapshot(root)


def write_snapshot(root=".", output_path=None):
    snapshot = build_snapshot(root=root)

    target = Path(output_path) if output_path else DEFAULT_OUTPUT_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return snapshot


if __name__ == "__main__":
    print(json.dumps(write_snapshot(), indent=2, sort_keys=True))

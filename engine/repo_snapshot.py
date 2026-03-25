import json
import os
import time
from pathlib import Path


TRACE_LOG_PATH = Path("brain_reports/repo_snapshot_trace.jsonl")


def _safe_read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


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
        "has_cge": snapshot.get("has_cge"),
        "cge_state": snapshot.get("cge_state"),
        "incoming_cge_bundles": snapshot.get("incoming_cge_bundles", []),
        "installed_cge_bundles": snapshot.get("installed_cge_bundles", []),
        "failed_cge_bundles": snapshot.get("failed_cge_bundles", []),
    }

    with TRACE_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")


def build_snapshot(root="."):
    root = Path(root)
    files = []
    tests = []

    for p in root.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(root)).replace("\\", "/")
            files.append(rel)
            if p.name.startswith("test_") or "/tests/" in f"/{rel}/" or "test" in p.name.lower():
                tests.append(rel)

    buildout_registry = _safe_read_json(root / ".buildout_registry.json") or {}
    phase_registry = _safe_read_json(root / ".buildout_phase_registry.json") or {}

    cge_info = _find_cge_bundle_state(root)

    snapshot = {
        "root": str(root),
        "file_count": len(files),
        "test_count": len(tests),
        "files": files[:100],
        "tests": tests[:100],
        "registry_entry_count": len(buildout_registry),
        "phase_registry_entry_count": len(phase_registry),
        "latest_global_root": None,
        "has_pending_bundles": cge_info["incoming_bundle_count"] > 0,
        "snapshot_source_module": __name__,
        "snapshot_source_file": __file__,
        **cge_info,
    }

    _trace_snapshot(snapshot)
    return snapshot


def snapshot_repo_state(root="."):
    return build_snapshot(root)

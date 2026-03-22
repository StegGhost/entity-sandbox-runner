from pathlib import Path
import json

def _safe_read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

def build_snapshot(root="."):
    root = Path(root)
    files = []
    tests = []

    for p in root.rglob("*"):
        if p.is_file():
            rel = str(p.relative_to(root))
            files.append(rel)
            if "test" in p.name.lower() or "tests/" in rel.replace("\\", "/"):
                tests.append(rel)

    buildout_registry = _safe_read_json(root / ".buildout_registry.json") or {}
    phase_registry = _safe_read_json(root / ".buildout_phase_registry.json") or {}
    latest_root = _safe_read_json(root / ".cge_store" / "latest_root.json") or {}

    return {
        "root": str(root),
        "file_count": len(files),
        "test_count": len(tests),
        "files": files[:100],
        "tests": tests[:100],
        "registry_entry_count": len(buildout_registry),
        "phase_registry_entry_count": len(phase_registry),
        "latest_global_root": latest_root.get("global_root"),
        "has_cge": latest_root.get("global_root") is not None,
    }

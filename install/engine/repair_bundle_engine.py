from pathlib import Path
from typing import Dict, Any, List
import json
import zipfile
import shutil
from datetime import datetime

ALLOWED_ROOTS = {
    "bundle_manifest.json",
    "install/",
    "install/engine/",
    "install/tests/",
}

OUTPUT_DIR = "fixed_bundles"
REPORT_DIR = "repair_reports"


def _now():
    return datetime.utcnow().isoformat()


def _safe_read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def _ensure_dirs(root: Path):
    (root / OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    (root / REPORT_DIR).mkdir(parents=True, exist_ok=True)


def _is_allowed(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in ALLOWED_ROOTS)


def _filter_files(file_list: List[str]) -> Dict[str, List[str]]:
    allowed = []
    removed = []

    for f in file_list:
        if _is_allowed(f):
            allowed.append(f)
        else:
            removed.append(f)

    return {
        "allowed": allowed,
        "removed": removed
    }


def _extract_bundle(zip_path: Path, extract_to: Path) -> List[str]:
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(extract_to)
        return z.namelist()


def _create_fixed_bundle(root: Path, source_dir: Path, files: List[str], output_name: str) -> Path:
    output_path = root / OUTPUT_DIR / output_name

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for rel_path in files:
            full_path = source_dir / rel_path
            if full_path.exists():
                z.write(full_path, rel_path)

    return output_path


def _write_report(root: Path, report: Dict[str, Any], name: str):
    path = root / REPORT_DIR / name
    path.write_text(json.dumps(report, indent=2))


def repair_bundle(state: Dict[str, Any]) -> Dict[str, Any]:
    root = Path(state["root"])

    action = state.get("next_action", {})
    target = action.get("target")

    if not target:
        return {
            "status": "noop",
            "reason": "no_target_provided"
        }

    bundle_path = root / target

    if not bundle_path.exists():
        return {
            "status": "failed",
            "reason": "bundle_not_found",
            "target": target
        }

    _ensure_dirs(root)

    temp_dir = root / "_repair_tmp"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)

    try:
        original_files = _extract_bundle(bundle_path, temp_dir)

        filtered = _filter_files(original_files)

        fixed_name = bundle_path.stem + "_fixed.zip"
        fixed_bundle_path = _create_fixed_bundle(
            root,
            temp_dir,
            filtered["allowed"],
            fixed_name
        )

        report = {
            "timestamp": _now(),
            "original_bundle": str(bundle_path.relative_to(root)),
            "fixed_bundle": str(fixed_bundle_path.relative_to(root)),
            "original_file_count": len(original_files),
            "allowed_file_count": len(filtered["allowed"]),
            "removed_file_count": len(filtered["removed"]),
            "removed_files": filtered["removed"],
            "status": "repaired"
        }

        report_name = fixed_name.replace(".zip", ".json")
        _write_report(root, report, report_name)

        return {
            "status": "ok",
            "action": "bundle_repaired",
            "fixed_bundle": str(fixed_bundle_path.relative_to(root)),
            "report": str((root / REPORT_DIR / report_name).relative_to(root)),
            "removed_files": filtered["removed"],
            "kept_files": filtered["allowed"]
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "target": target
        }

    finally:
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

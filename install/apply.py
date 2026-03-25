import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path.cwd()
INSTALL_DIR = ROOT / "install"
ENGINE_DIR = ROOT / "engine"
TESTS_DIR = ROOT / "tests"

REPORT_PATH = ROOT / "brain_reports" / "apply_result.json"


# -------------------------
# UTIL
# -------------------------

def ensure_dirs():
    ENGINE_DIR.mkdir(exist_ok=True)
    TESTS_DIR.mkdir(exist_ok=True)
    (ROOT / "brain_reports").mkdir(exist_ok=True)


def load_manifest():
    manifest_path = INSTALL_DIR / "bundle_manifest.json"
    if not manifest_path.exists():
        return None

    try:
        with open(manifest_path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def extract_family(name):
    return name.split("_v")[0]


# -------------------------
# VALIDATION
# -------------------------

def validate_paths(manifest):
    if not manifest:
        return True, "no_manifest_fallback"

    allowed = manifest.get("allowed_paths", [])
    if not allowed:
        return False, "missing_allowed_paths"

    return True, "ok"


def is_allowed_path(rel_path, allowed_paths):
    if not allowed_paths:
        return True

    for allowed in allowed_paths:
        if rel_path.startswith(allowed):
            return True
    return False


# -------------------------
# COPY ENGINE
# -------------------------

def copy_tree(src_root, dst_root, allowed_paths):
    copied = []
    rejected = []

    if not src_root.exists():
        return copied, rejected

    for p in src_root.rglob("*"):
        if not p.is_file():
            continue

        rel = str(p.relative_to(INSTALL_DIR)).replace("\\", "/")

        if not is_allowed_path(rel, allowed_paths):
            rejected.append(rel)
            continue

        # map install/engine/... → engine/...
        if rel.startswith("install/engine/"):
            target = dst_root / "engine" / rel.replace("install/engine/", "")
        elif rel.startswith("install/tests/"):
            target = dst_root / "tests" / rel.replace("install/tests/", "")
        else:
            # skip anything not explicitly mapped
            rejected.append(rel)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        copied.append(str(target))

    return copied, rejected


# -------------------------
# MAIN APPLY
# -------------------------

def apply_bundle():
    ensure_dirs()

    manifest = load_manifest()

    valid, reason = validate_paths(manifest)
    if not valid:
        return {
            "status": "failed",
            "failure_type": "manifest_invalid",
            "reason": reason
        }

    allowed_paths = manifest.get("allowed_paths", []) if manifest else []

    copied, rejected = copy_tree(INSTALL_DIR, ROOT, allowed_paths)

    if not copied:
        return {
            "status": "failed",
            "failure_type": "no_valid_files",
            "copied_count": 0,
            "rejected_count": len(rejected)
        }

    return {
        "status": "ok",
        "copied_count": len(copied),
        "rejected_count": len(rejected),
        "copied_files": copied[:10],  # capped for sanity
        "rejected_files": rejected[:10],
        "verification": {
            "manifest_present": manifest is not None,
            "mode": reason
        }
    }


# -------------------------
# ENTRYPOINT
# -------------------------

def main():
    result = apply_bundle()

    output = {
        "generated_at": datetime.utcnow().isoformat(),
        "result": result
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

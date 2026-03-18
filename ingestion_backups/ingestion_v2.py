import os
import json
import shutil
import zipfile
import time

INCOMING = "incoming_bundles"
INSTALLED = "installed_bundles"
FAILED = "failed_bundles"
LOG = "logs/ingestion_log.json"

ALLOWED_PREFIXES = (
    "install/",
    "payload/",
    "experiments/",
    "workflow_review/",
    "config/",
)

REPO_ROOT_PREFIX = "payload/repo_root/"

IGNORE_PREFIXES = (
    "__MACOSX/",
)

IGNORE_NAMES = (
    ".DS_Store",
)

def _ensure():
    os.makedirs(INCOMING, exist_ok=True)
    os.makedirs(INSTALLED, exist_ok=True)
    os.makedirs(FAILED, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

def _load_log():
    if os.path.exists(LOG) and os.path.getsize(LOG) > 0:
        try:
            with open(LOG, "r") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def _save_log(log):
    with open(LOG, "w") as f:
        json.dump(log, f, indent=2)

def _safe_json_load(path):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return {}
        with open(path, "r") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}

def _is_ignored_member(name):
    if any(name.startswith(prefix) for prefix in IGNORE_PREFIXES):
        return True
    base = os.path.basename(name.rstrip("/"))
    if base in IGNORE_NAMES:
        return True
    return False

def _is_allowed_member(name):
    if name == "bundle_manifest.json":
        return True
    return any(name.startswith(prefix) for prefix in ALLOWED_PREFIXES)

def _validate_manifest(manifest):
    required = ["bundle_name", "bundle_version", "install_mode"]
    missing = [k for k in required if k not in manifest]
    if missing:
        raise Exception(f"manifest_missing_fields:{missing}")

    if manifest.get("install_mode") != "folder_map":
        raise Exception("unsupported_install_mode")

def _repo_destination(rel_path):
    if rel_path.startswith(REPO_ROOT_PREFIX):
        repo_rel = rel_path[len(REPO_ROOT_PREFIX):]
        if not repo_rel:
            raise Exception("empty_repo_root_mapping")
        return repo_rel
    return rel_path

def _install_zip(path):
    tmp = f"_tmp_ingest_{int(time.time() * 1000)}"
    os.makedirs(tmp, exist_ok=True)

    try:
        with zipfile.ZipFile(path, "r") as z:
            names = z.namelist()
            if "bundle_manifest.json" not in names:
                raise Exception("missing_bundle_manifest")

            manifest_file = z.extract("bundle_manifest.json", tmp)
            manifest = _safe_json_load(manifest_file)
            _validate_manifest(manifest)

            filtered_names = []
            for n in names:
                if n.endswith("/"):
                    continue
                if _is_ignored_member(n):
                    continue
                if not _is_allowed_member(n):
                    raise Exception(f"path_not_allowed:{n}")
                filtered_names.append(n)

            for n in filtered_names:
                z.extract(n, tmp)

        for root, _, files in os.walk(tmp):
            for file in files:
                src = os.path.join(root, file)
                rel = os.path.relpath(src, tmp)

                if rel == "bundle_manifest.json":
                    continue
                if _is_ignored_member(rel):
                    continue

                dst = _repo_destination(rel)

                if dst == ".git" or dst.startswith(".git/"):
                    raise Exception(f"forbidden_destination:{dst}")

                parent = os.path.dirname(dst)
                if parent:
                    os.makedirs(parent, exist_ok=True)

                shutil.copy2(src, dst)

        shutil.rmtree(tmp, ignore_errors=True)
        return True, None

    except Exception as e:
        shutil.rmtree(tmp, ignore_errors=True)
        return False, str(e)

def process():
    _ensure()
    log = _load_log()

    files = sorted(f for f in os.listdir(INCOMING) if f.endswith(".zip"))

    for f in files:
        src = os.path.join(INCOMING, f)
        ok, err = _install_zip(src)

        entry = {
            "bundle": f,
            "ok": ok,
            "error": err,
            "ts": time.time()
        }
        log.append(entry)

        if ok:
            shutil.move(src, os.path.join(INSTALLED, f))
        else:
            shutil.move(src, os.path.join(FAILED, f))

    _save_log(log)

if __name__ == "__main__":
    process()

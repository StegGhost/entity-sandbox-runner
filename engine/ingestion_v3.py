import os
import json
import zipfile
import time
import shutil

ROOT = os.getcwd()

INCOMING = os.path.join(ROOT, "incoming_bundles")
INSTALLED = os.path.join(ROOT, "installed_bundles")
FAILED = os.path.join(ROOT, "failed_bundles")

LOG_PATH = os.path.join(ROOT, "logs", "ingestion_log.json")
REPORTS_DIR = os.path.join(ROOT, "ingestion_reports")


def ensure_dirs():
    os.makedirs(INCOMING, exist_ok=True)
    os.makedirs(INSTALLED, exist_ok=True)
    os.makedirs(FAILED, exist_ok=True)
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)


def load_log():
    if not os.path.exists(LOG_PATH):
        return []
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def write_log(log):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)
        f.write("\n")


def write_report(bundle, ok, error=None):
    report = {
        "bundle": bundle,
        "ok": ok,
        "error": error,
        "ts": time.time()
    }

    path = os.path.join(REPORTS_DIR, f"{bundle}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        f.write("\n")


def load_manifest(zf):
    try:
        with zf.open("bundle_manifest.json") as f:
            return json.load(f)
    except Exception:
        return None


def is_allowed(member, allowed_paths):
    normalized = member.strip("/")

    for p in allowed_paths:
        base = str(p).strip("/")
        if not base:
            continue

        if base.endswith("/"):
            base = base.rstrip("/")

        if normalized == base or normalized.startswith(base + "/"):
            return True

    return False


def validate_bundle(zf, manifest):
    if not manifest:
        return False, "missing_bundle_manifest"

    required = ["bundle_name", "bundle_version", "install_mode", "allowed_paths"]
    missing = [r for r in required if r not in manifest]
    if missing:
        return False, f"manifest_missing_fields:{missing}"

    if manifest.get("install_mode") != "folder_map":
        return False, "unsupported_install_mode"

    allowed_paths = manifest.get("allowed_paths", [])
    if not isinstance(allowed_paths, list) or not allowed_paths:
        return False, "missing_allowed_paths"

    for member in zf.namelist():
        if not member or member.endswith("/"):
            continue
        if not is_allowed(member, allowed_paths):
            return False, f"path_not_allowed:{member}"

    return True, None


def install_bundle(bundle_path):
    bundle_name = os.path.basename(bundle_path)
    log = load_log()

    try:
        with zipfile.ZipFile(bundle_path, "r") as zf:
            manifest = load_manifest(zf)
            ok, error = validate_bundle(zf, manifest)
            if not ok:
                raise Exception(error)

            zf.extractall(ROOT)

        destination = os.path.join(INSTALLED, bundle_name)
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(bundle_path, destination)

        log.append({"bundle": bundle_name, "ok": True, "error": None, "ts": time.time()})
        write_log(log)
        write_report(bundle_name, True)

    except Exception as e:
        destination = os.path.join(FAILED, bundle_name)
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(bundle_path, destination)

        log.append({"bundle": bundle_name, "ok": False, "error": str(e), "ts": time.time()})
        write_log(log)
        write_report(bundle_name, False, str(e))


def run():
    ensure_dirs()
    for fname in sorted(os.listdir(INCOMING)):
        if not fname.endswith(".zip"):
            continue
        full_path = os.path.join(INCOMING, fname)
        if os.path.isfile(full_path):
            install_bundle(full_path)


if __name__ == "__main__":
    run()


import os, json, shutil, zipfile, time

INCOMING = "incoming_bundles"
INSTALLED = "installed_bundles"
FAILED = "failed_bundles"
LOG = "logs/ingestion_log.json"

def _ensure():
    os.makedirs(INCOMING, exist_ok=True)
    os.makedirs(INSTALLED, exist_ok=True)
    os.makedirs(FAILED, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

def _load_log():
    if os.path.exists(LOG):
        try:
            return json.load(open(LOG))
        except:
            return []
    return []

def _save_log(log):
    json.dump(log, open(LOG, "w"), indent=2)

def _is_valid_member(name):
    allowed = ("install/", "payload/", "experiments/", "workflow_review/")
    return any(name.startswith(p) for p in allowed)

def _install_zip(path):
    tmp = f"_tmp_ingest_{int(time.time()*1000)}"
    os.makedirs(tmp, exist_ok=True)

    try:
        with zipfile.ZipFile(path, "r") as z:
            names = z.namelist()
            if "bundle_manifest.json" not in names:
                raise Exception("missing bundle_manifest.json")

            for n in names:
                if n.endswith("/"):
                    continue
                if n == "bundle_manifest.json":
                    continue
                if not _is_valid_member(n):
                    raise Exception(f"path not allowed: {n}")

            z.extractall(tmp)

        # copy files into repo root
        for root, dirs, files in os.walk(tmp):
            for file in files:
                src = os.path.join(root, file)
                rel = os.path.relpath(src, tmp)
                if rel == "bundle_manifest.json":
                    continue
                dst = rel
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)

        shutil.rmtree(tmp, ignore_errors=True)
        return True, None

    except Exception as e:
        shutil.rmtree(tmp, ignore_errors=True)
        return False, str(e)

def process():
    _ensure()
    log = _load_log()

    files = [f for f in os.listdir(INCOMING) if f.endswith(".zip")]
    files.sort()

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

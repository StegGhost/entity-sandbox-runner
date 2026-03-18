
import os, json, hashlib, shutil

CANONICAL_ROOT = "payload/canonical_repo/adaptive_v20"
PROFILE_PATH = "config/experiment_profiles.json"

def sha(path):
    try:
        with open(path,"rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def load_profile():
    with open(PROFILE_PATH) as f:
        return json.load(f)["profiles"]["adaptive_v20"]

def ensure(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def repair(file):
    src = os.path.join(CANONICAL_ROOT, file)
    if not os.path.exists(src):
        return False
    ensure(file)
    shutil.copy2(src, file)
    return True

def run_preflight():
    profile = load_profile()
    files = profile["required_files"]

    drift = []
    for f in files:
        h1 = sha(f)
        h2 = sha(os.path.join(CANONICAL_ROOT, f))

        if h2 is None:
            drift.append((f,"missing_canonical"))
        elif h1 != h2:
            drift.append((f,"repair"))

    repairs = []
    for f,status in drift:
        if status == "repair":
            if repair(f):
                repairs.append(f)

    # re-check
    final = []
    for f in files:
        if sha(f) != sha(os.path.join(CANONICAL_ROOT,f)):
            final.append(f)

    return {
        "status": "pass" if not final else "fail",
        "repairs": repairs,
        "remaining": final
    }

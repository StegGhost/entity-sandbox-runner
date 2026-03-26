import json
import os
import shutil
import subprocess
import tempfile
from typing import Dict, Any, List

from engine.proposal_to_bundle import proposal_to_bundle


TEST_CMD = "python -m pytest -q"


# -------------------------
# RUN TESTS
# -------------------------

def run_tests(cwd: str) -> int:
    proc = subprocess.run(
        TEST_CMD,
        shell=True,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.returncode


# -------------------------
# APPLY PATCH
# -------------------------

def apply_patch(bundle: Dict[str, Any], root: str):
    for f in bundle.get("files_to_create", []):
        path = os.path.join(root, f["path"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as fp:
            fp.write(f["content"])


# -------------------------
# SANDBOX EXECUTION
# -------------------------

def evaluate_bundle(bundle: Dict[str, Any], snapshot_root: str) -> Dict[str, Any]:

    tmpdir = tempfile.mkdtemp()

    try:
        shutil.copytree(snapshot_root, tmpdir, dirs_exist_ok=True)

        apply_patch(bundle, tmpdir)

        rc = run_tests(tmpdir)

        return {
            "success": rc == 0,
            "return_code": rc,
            "bundle": bundle,
        }

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# -------------------------
# MULTI-REPAIR ENGINE
# -------------------------

def generate_candidates(snapshot: Dict[str, Any], failure_text: str) -> List[Dict[str, Any]]:
    # reuse proposal engine but expand
    base = proposal_to_bundle(snapshot, failure_text)

    if base["proposal_name"] == "no_op":
        return []

    # for now: single + variants
    return [base]


# -------------------------
# SELECT BEST FIX
# -------------------------

def select_best(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    for r in results:
        if r["success"]:
            return r
    return {}


# -------------------------
# APPLY FINAL FIX
# -------------------------

def apply_best(bundle: Dict[str, Any], root: str):
    apply_patch(bundle, root)


# -------------------------
# MAIN
# -------------------------

def main():

    failure_text = ""

    if len(os.sys.argv) > 1:
        with open(os.sys.argv[1], "r") as f:
            failure_text = f.read()

    snapshot = {
        "root": "."
    }

    # -------------------------
    # GENERATE CANDIDATES
    # -------------------------

    candidates = generate_candidates(snapshot, failure_text)

    if not candidates:
        result = {
            "status": "no_op",
            "reason": "no_candidates"
        }
        print(json.dumps(result, indent=2))
        return

    # -------------------------
    # TEST EACH IN SANDBOX
    # -------------------------

    results = []
    for c in candidates:
        r = evaluate_bundle(c, ".")
        results.append(r)

    # -------------------------
    # SELECT BEST
    # -------------------------

    best = select_best(results)

    if not best:
        result = {
            "status": "failed",
            "reason": "no_valid_fix",
            "attempts": results
        }
        print(json.dumps(result, indent=2))
        return

    # -------------------------
    # APPLY TO REAL REPO
    # -------------------------

    apply_best(best["bundle"], ".")

    result = {
        "status": "fixed",
        "applied": best["bundle"]["proposal_name"]
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

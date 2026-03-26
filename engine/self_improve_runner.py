import os
import json
import shutil
import subprocess
import time
import multiprocessing

from engine.repo_snapshot import generate_snapshot
from engine.llm_self_improve import generate_proposals

BASE_SANDBOX = "sandbox_runs"
RESULT_PATH = "brain_reports/apply_result.json"
QUARANTINE = "quarantine_patches"


# =========================
# TEST EXECUTION
# =========================

def run_tests(cwd):
    proc = subprocess.run(
        "python -m pytest -q",
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return proc.returncode, proc.stdout + proc.stderr


def score(rc, out):
    score = 0
    if rc == 0:
        score += 100
    score -= out.count("FAILED") * 10
    score -= out.count("ERROR") * 5
    return score


# =========================
# SANDBOX RUNNER
# =========================

def run_candidate(args):
    idx, proposal = args
    sandbox = f"{BASE_SANDBOX}/run_{idx}"

    if os.path.exists(sandbox):
        shutil.rmtree(sandbox)

    shutil.copytree(".", sandbox,
        ignore=shutil.ignore_patterns("__pycache__", ".git", BASE_SANDBOX, "brain_reports")
    )

    # apply patch
    for f in proposal["files"]:
        p = os.path.join(sandbox, f["path"])
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as out:
            out.write(f["content"])

    rc, out = run_tests(sandbox)
    return {
        "proposal": proposal,
        "score": score(rc, out),
        "rc": rc,
        "output": out[:1000]
    }


# =========================
# MAIN LOOP
# =========================

def main(failure_file=None):

    failure_text = ""
    if failure_file and os.path.exists(failure_file):
        with open(failure_file) as f:
            failure_text = f.read()

    snapshot = generate_snapshot(".")

    gen = generate_proposals(snapshot, failure_text)

    if not gen["proposals"]:
        print("No proposals")
        return

    os.makedirs(BASE_SANDBOX, exist_ok=True)

    pool = multiprocessing.Pool(processes=min(4, len(gen["proposals"])))
    results = pool.map(run_candidate, list(enumerate(gen["proposals"])))
    pool.close()
    pool.join()

    best = max(results, key=lambda x: x["score"])

    applied = False

    # apply only if improvement
    if best["score"] > 0:
        for f in best["proposal"]["files"]:
            os.makedirs(os.path.dirname(f["path"]), exist_ok=True)
            with open(f["path"], "w") as out:
                out.write(f["content"])
        applied = True
    else:
        os.makedirs(QUARANTINE, exist_ok=True)
        with open(f"{QUARANTINE}/failed_{int(time.time())}.json", "w") as f:
            json.dump(results, f, indent=2)

    result = {
        "classification": gen["classification"],
        "candidates": results,
        "best": best,
        "applied": applied,
        "ts": time.time()
    }

    os.makedirs("brain_reports", exist_ok=True)
    with open(RESULT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)

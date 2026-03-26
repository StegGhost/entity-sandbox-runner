import json
import os
import shutil
import subprocess
import zipfile
import time

from engine.repo_snapshot import generate_snapshot
from engine.llm_self_improve import generate_proposals

SANDBOX_BASE = "sandbox_runs"
RESULT_PATH = "brain_reports/apply_result.json"


def run_tests():
    result = subprocess.run(
        "python -m pytest -q",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout + "\n" + result.stderr


def apply_patch(files, sandbox_dir):
    for f in files:
        path = os.path.join(sandbox_dir, f["path"])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as out:
            out.write(f["content"])


def copy_repo_to_sandbox(sandbox_dir):
    if os.path.exists(sandbox_dir):
        shutil.rmtree(sandbox_dir)

    shutil.copytree(".", sandbox_dir, ignore=shutil.ignore_patterns(
        "__pycache__", ".git", SANDBOX_BASE, "brain_reports"
    ))


def score_result(returncode, output):
    score = 0

    if returncode == 0:
        score += 100

    failures = output.count("FAILED")
    errors = output.count("ERROR")

    score -= failures * 10
    score -= errors * 5

    return score


def main(failure_file=None):

    failure_text = ""
    if failure_file and os.path.exists(failure_file):
        with open(failure_file, "r") as f:
            failure_text = f.read()

    snapshot = generate_snapshot(".")

    result = generate_proposals(snapshot, failure_text)

    if result["status"] != "candidates_generated":
        print(json.dumps(result, indent=2))
        return

    proposals = result["proposals"]

    best_score = -9999
    best = None

    os.makedirs(SANDBOX_BASE, exist_ok=True)

    for i, proposal in enumerate(proposals):

        sandbox_dir = os.path.join(SANDBOX_BASE, f"run_{i}")

        copy_repo_to_sandbox(sandbox_dir)

        apply_patch(proposal.get("files_to_create", []), sandbox_dir)

        cwd = os.getcwd()
        os.chdir(sandbox_dir)

        rc, output = run_tests()
        score = score_result(rc, output)

        os.chdir(cwd)

        if score > best_score:
            best_score = score
            best = {
                "proposal": proposal,
                "score": score,
                "output": output[:1000]
            }

    # =========================
    # APPLY BEST (SAFE)
    # =========================

    applied = False

    if best and best["score"] > 0:
        for f in best["proposal"].get("files_to_create", []):
            path = f["path"]
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as out:
                out.write(f["content"])
        applied = True

    result = {
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

import json
import os
import subprocess
import zipfile
import time

from engine.repo_snapshot import generate_snapshot
from engine.llm_self_improve import generate_proposal

INCOMING = "incoming_bundles"
SANDBOX = "sandbox_workspace"
RESULT_PATH = "brain_reports/apply_result.json"


def run_tests():
    result = subprocess.run(
        "python -m pytest -q",
        shell=True,
        capture_output=True,
        text=True
    )
    return result.stdout + "\n" + result.stderr


def build_bundle(proposal):
    ts = int(time.time())
    bundle_name = f"auto_repair_{proposal['proposal_name']}_{ts}.zip"
    bundle_path = os.path.join(INCOMING, bundle_name)

    os.makedirs(INCOMING, exist_ok=True)

    with zipfile.ZipFile(bundle_path, "w") as z:
        for f in proposal.get("files_to_create", []):
            tmp_path = f"/tmp/{os.path.basename(f['path'])}"
            with open(tmp_path, "w") as tmp:
                tmp.write(f["content"])
            z.write(tmp_path, f["path"])

    return bundle_path


def apply_bundle(bundle_path):
    try:
        with zipfile.ZipFile(bundle_path, "r") as z:
            z.extractall(SANDBOX)

        for root, _, files in os.walk(SANDBOX):
            for f in files:
                src = os.path.join(root, f)
                dst = os.path.relpath(src, SANDBOX)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(src, "rb") as s, open(dst, "wb") as d:
                    d.write(s.read())

        return {"status": "applied"}

    except Exception as e:
        return {"status": "failed", "error": str(e)}


def main(failure_file=None):

    failure_text = ""
    if failure_file and os.path.exists(failure_file):
        with open(failure_file, "r") as f:
            failure_text = f.read()

    snapshot = generate_snapshot(".")

    result = generate_proposal(snapshot, failure_text)

    if result["status"] != "repair_generated":
        print(json.dumps(result, indent=2))
        return

    proposal = result["proposal"]

    bundle_path = build_bundle(proposal)

    apply_result = apply_bundle(bundle_path)

    post_test_output = run_tests()

    final = {
        "proposal": proposal,
        "bundle": bundle_path,
        "apply_result": apply_result,
        "post_test_output": post_test_output[:2000]
    }

    os.makedirs("brain_reports", exist_ok=True)
    with open(RESULT_PATH, "w") as f:
        json.dump(final, f, indent=2)

    print(json.dumps(final, indent=2))


if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    main(arg)


import os, json

REQUIRED = [
    "config/policy.json",
    "experiments/evaluation_suite/run_eval.py",
    "install/ingestion_v2.py"
]

CANONICAL = "payload/canonical_repo/default"

def _exists(p):
    return os.path.exists(p)

def _repair_from_canonical():
    if not os.path.exists(CANONICAL):
        return []
    repaired = []
    for root, dirs, files in os.walk(CANONICAL):
        for f in files:
            src = os.path.join(root, f)
            rel = os.path.relpath(src, CANONICAL)
            dst = rel
            if not os.path.exists(dst):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with open(src, "rb") as s, open(dst, "wb") as d:
                    d.write(s.read())
                repaired.append(dst)
    return repaired

def run_preflight():
    report = {
        "status": "pass",
        "missing": [],
        "repaired": []
    }

    for r in REQUIRED:
        if not _exists(r):
            report["missing"].append(r)

    if report["missing"]:
        report["repaired"] = _repair_from_canonical()
        # re-check
        still = [r for r in REQUIRED if not _exists(r)]
        if still:
            report["status"] = "fail"
            report["missing"] = still

    os.makedirs("logs", exist_ok=True)
    json.dump(report, open("logs/preflight.json", "w"), indent=2)

    if report["status"] != "pass":
        raise Exception("preflight failed")

    return report

if __name__ == "__main__":
    run_preflight()

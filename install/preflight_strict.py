import argparse
import json
import os
import shutil
from typing import Dict, Any, List

REQUIRED = [
    "config/policy.json",
    "experiments/evaluation_suite/run_eval.py",
    "install/ingestion_v2.py"
]

CANONICAL = "payload/canonical_repo/default"
LOG_PATH = "logs/preflight.json"


def _exists(path: str) -> bool:
    return os.path.exists(path)


def _ensure_parent(path: str):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def _repair_from_canonical() -> List[str]:
    if not os.path.exists(CANONICAL):
        return []

    repaired = []

    for root, _, files in os.walk(CANONICAL):
        for name in files:
            src = os.path.join(root, name)
            rel = os.path.relpath(src, CANONICAL)
            dst = rel

            if not os.path.exists(dst):
                _ensure_parent(dst)
                with open(src, "rb") as s, open(dst, "wb") as d:
                    d.write(s.read())
                repaired.append(dst)

    return repaired


def _write_report(report: Dict[str, Any]):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)


def run_preflight(required_files: List[str] = None) -> Dict[str, Any]:
    if required_files is None:
        required_files = REQUIRED

    report: Dict[str, Any] = {
        "status": "pass",
        "missing": [],
        "repaired": [],
        "required": required_files,
        "canonical_root": CANONICAL
    }

    for path in required_files:
        if not _exists(path):
            report["missing"].append(path)

    if report["missing"]:
        report["repaired"] = _repair_from_canonical()

        still_missing = [path for path in required_files if not _exists(path)]
        if still_missing:
            report["status"] = "fail"
            report["missing"] = still_missing
        else:
            report["status"] = "pass"
            report["missing"] = []

    _write_report(report)
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Strict required-file preflight with canonical restore."
    )
    parser.add_argument(
        "--required-json",
        default="",
        help="Optional JSON array of required file paths."
    )
    args = parser.parse_args()

    required_files = REQUIRED
    if args.required_json:
        try:
            parsed = json.loads(args.required_json)
            if isinstance(parsed, list):
                required_files = [str(x) for x in parsed]
        except Exception:
            pass

    report = run_preflight(required_files=required_files)

    print(json.dumps(report, indent=2))

    if report["status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

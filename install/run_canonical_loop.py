import json
import os
import subprocess
import sys
import time

CONFIG_PATH = "config/canonical_loop_config.json"


DEFAULT_CONFIG = {
    "run_compactor": True,
    "run_feedback": True,
    "python_executable": sys.executable,
    "compactor_script": "install/document_compactor.py",
    "feedback_script": "install/canonical_feedback.py",
    "commit_targets": [
        "docs/canonical",
        "payload/feedback",
        "payload/receipts/document_compaction",
        "payload/receipts/canonical_feedback"
    ]
}


def _load_config():
    if not os.path.exists(CONFIG_PATH) or os.path.getsize(CONFIG_PATH) == 0:
        return DEFAULT_CONFIG.copy()
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return DEFAULT_CONFIG.copy()
        merged = DEFAULT_CONFIG.copy()
        merged.update(data)
        return merged
    except Exception:
        return DEFAULT_CONFIG.copy()


def _run_step(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "cmd": cmd,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def main():
    cfg = _load_config()
    py = cfg.get("python_executable", sys.executable)
    report = {
        "timestamp": time.time(),
        "steps": []
    }

    if cfg.get("run_compactor", True):
        report["steps"].append(_run_step([py, cfg.get("compactor_script", "install/document_compactor.py")]))

    if cfg.get("run_feedback", True):
        report["steps"].append(_run_step([py, cfg.get("feedback_script", "install/canonical_feedback.py")]))

    ok = all(step["returncode"] == 0 for step in report["steps"])
    report["status"] = "ok" if ok else "failed"

    os.makedirs("payload/feedback", exist_ok=True)
    out_path = "payload/feedback/canonical_loop_report.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "status": report["status"],
        "report_path": out_path,
        "steps": [{"cmd": s["cmd"], "returncode": s["returncode"]} for s in report["steps"]]
    }, indent=2, ensure_ascii=False))

    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

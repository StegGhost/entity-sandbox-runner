import subprocess
import json
import time
import os
import traceback

DEFAULT_CONFIG = {
    "max_retries": 2,
    "retry_backoff_seconds": 2,
    "continue_on_failure": False,
    "receipts_root": "payload/receipts/failure_recovery",
    "report_path": "payload/runtime/failure_recovery_report.json"
}

STEPS = [
    ("document_compactor", ["python", "install/document_compactor.py"]),
    ("canonical_feedback", ["python", "install/canonical_feedback.py"]),
    ("knowledge_delta", ["python", "install/knowledge_delta.py"]),
    ("canonical_receipt_binder", ["python", "install/canonical_receipt_binder.py"]),
    ("feedback_injection", ["python", "install/feedback_injection.py"]),
    ("feedback_execution_bridge", ["python", "install/feedback_execution_bridge.py"]),
]

def _load_json(path, default):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _classify_failure(stderr, returncode):
    s = (stderr or "").lower()
    if returncode == 0:
        return "none"
    if "no such file" in s or "not found" in s:
        return "missing_dependency"
    if "permission denied" in s:
        return "permission_error"
    if "json" in s and ("decode" in s or "expecting" in s):
        return "data_corruption"
    if "timeout" in s:
        return "timeout"
    return "unknown_error"

def _sha256_obj(obj):
    import hashlib
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8", errors="replace")
    return hashlib.sha256(raw).hexdigest()

def run_step(name, cmd, cfg):
    attempts = []
    for i in range(cfg["max_retries"] + 1):
        start = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            rc = result.returncode
            out = result.stdout
            err = result.stderr
        except Exception as e:
            rc = 1
            out = ""
            err = traceback.format_exc()

        duration = time.time() - start
        classification = _classify_failure(err, rc)

        attempt = {
            "attempt": i + 1,
            "cmd": cmd,
            "returncode": rc,
            "stdout": out,
            "stderr": err,
            "duration_seconds": duration,
            "classification": classification
        }
        attempts.append(attempt)

        if rc == 0:
            return {
                "step": name,
                "status": "ok",
                "attempts": attempts
            }

        # retry if not last attempt
        if i < cfg["max_retries"]:
            time.sleep(cfg["retry_backoff_seconds"] * (i + 1))

    return {
        "step": name,
        "status": "failed",
        "attempts": attempts
    }

def main():
    cfg = _load_json("config/failure_recovery_config.json", DEFAULT_CONFIG)
    merged = DEFAULT_CONFIG.copy()
    merged.update(cfg)

    os.makedirs(os.path.dirname(merged["report_path"]), exist_ok=True)
    os.makedirs(merged["receipts_root"], exist_ok=True)

    report = {
        "timestamp": time.time(),
        "config": merged,
        "steps": []
    }

    overall_status = "ok"

    for name, cmd in STEPS:
        step_result = run_step(name, cmd, merged)
        report["steps"].append(step_result)

        if step_result["status"] != "ok":
            overall_status = "failed"
            if not merged.get("continue_on_failure", False):
                break

    report["status"] = overall_status

    # write report
    with open(merged["report_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # write receipt
    existing = sorted(
        f for f in os.listdir(merged["receipts_root"])
        if f.startswith("failure_recovery_") and f.endswith(".json")
    )
    receipt = {
        "type": "failure_recovery",
        "timestamp": report["timestamp"],
        "status": report["status"],
        "report_path": merged["report_path"]
    }
    receipt["hash"] = _sha256_obj(receipt)

    receipt_path = os.path.join(
        merged["receipts_root"],
        f"failure_recovery_{len(existing)+1:04d}.json"
    )

    with open(receipt_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2)

    print(json.dumps({
        "status": report["status"],
        "report": merged["report_path"],
        "receipt": receipt_path
    }, indent=2))

    if report["status"] != "ok":
        raise SystemExit(1)

if __name__ == "__main__":
    main()

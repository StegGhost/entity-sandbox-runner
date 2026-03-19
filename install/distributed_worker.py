import subprocess, json, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT = {
  "workers": 3,
  "steps": [
    ["python", "install/document_compactor.py"],
    ["python", "install/canonical_feedback.py"],
    ["python", "install/knowledge_delta.py"]
  ],
  "receipts_root": "payload/receipts/distributed_worker",
  "report_path": "payload/runtime/distributed_worker_report.json"
}

def _load(p, d):
    try:
        if not os.path.exists(p): return d
        with open(p, "r", encoding="utf-8") as f: return json.load(f)
    except Exception:
        return d

def run_cmd(cmd):
    start = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    return {
        "cmd": cmd,
        "returncode": r.returncode,
        "stdout": r.stdout,
        "stderr": r.stderr,
        "duration": time.time() - start
    }

def main():
    cfg = _load("config/distributed_worker_config.json", DEFAULT)
    merged = DEFAULT.copy(); merged.update(cfg)

    os.makedirs(os.path.dirname(merged["report_path"]), exist_ok=True)
    os.makedirs(merged["receipts_root"], exist_ok=True)

    results = []
    with ThreadPoolExecutor(max_workers=merged["workers"]) as ex:
        futures = [ex.submit(run_cmd, s) for s in merged["steps"]]
        for f in as_completed(futures):
            results.append(f.result())

    report = {"timestamp": time.time(), "results": results}
    with open(merged["report_path"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # receipt
    existing = [f for f in os.listdir(merged["receipts_root"]) if f.startswith("distributed_worker_")]
    rp = os.path.join(merged["receipts_root"], f"distributed_worker_{len(existing)+1:04d}.json")
    with open(rp, "w", encoding="utf-8") as f:
        json.dump({"type":"distributed_worker","timestamp":report["timestamp"],"report":merged["report_path"]}, f, indent=2)

    print(json.dumps({"status":"ok","report":merged["report_path"],"receipt":rp}, indent=2))

if __name__ == "__main__":
    main()

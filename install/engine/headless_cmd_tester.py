import argparse
import json
import time
import urllib.request
from pathlib import Path
from execution_hasher import compute_execution_hash

BASE_URL = "https://steggate-api.onrender.com"

REPORT_DIR = Path("brain_reports")


def http_post(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.getcode(), json.loads(resp.read().decode())


def http_get(url):
    with urllib.request.urlopen(url) as resp:
        return resp.getcode(), json.loads(resp.read().decode())


def run():
    REPORT_DIR.mkdir(exist_ok=True)

    report = {
        "mode": "steggate_bound_execution",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "ok",
        "steps": {}
    }

    # --- HEALTH ---
    code, data = http_get(f"{BASE_URL}/health")
    report["steps"]["health"] = {
        "ok": code == 200,
        "status_code": code,
        "data": data
    }

    # --- TOKEN ---
    code, data = http_post(f"{BASE_URL}/token", {})
    token = data.get("token")

    report["steps"]["token"] = {
        "ok": code == 200,
        "status_code": code,
        "data": data
    }

    # --- EXECUTION PAYLOAD ---
    execution_payload = {
        "t": 1,
        "system": "control_plane",
        "intent": "evidence_test"
    }

    execution_hash = compute_execution_hash(execution_payload)

    # --- EXECUTE ---
    code, data = http_post(
        f"{BASE_URL}/execute",
        {
            "token": token,
            "target": "https://httpbin.org/post",
            "payload": execution_payload,
            "execution_hash": execution_hash
        }
    )

    receipt = data.get("receipt", {})

    report["steps"]["execute"] = {
        "ok": code == 200,
        "status_code": code,
        "data": data
    }

    # --- VERIFY ---
    receipt_id = receipt.get("receipt_id")

    code, data = http_post(
        f"{BASE_URL}/verify",
        {"receipt_id": receipt_id}
    )

    report["steps"]["verify"] = {
        "ok": code == 200,
        "status_code": code,
        "data": data
    }

    # --- BINDING CHECK ---
    report["binding"] = {
        "execution_hash": execution_hash,
        "receipt_action_hash": receipt.get("action_hash"),
        "match": execution_hash == receipt.get("action_hash")
    }

    # --- FINAL STATUS ---
    if not report["binding"]["match"]:
        report["status"] = "invalid"
        report["reason"] = "execution_receipt_mismatch"

    out_json = REPORT_DIR / "headless_cmd_test.json"
    out_md = REPORT_DIR / "headless_cmd_test.md"

    out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
    out_md.write_text(f"# Headless Bound Execution\n\n```json\n{json.dumps(report, indent=2)}\n```")

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()

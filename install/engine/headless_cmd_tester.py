import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import requests

BASE_URL = "https://steggate-api.onrender.com"
REPORT_DIR = Path("brain_reports")


def stable_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_reports(report: dict):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = REPORT_DIR / "headless_cmd_test.json"
    md_path = REPORT_DIR / "headless_cmd_test.md"

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_lines = [
        "# Headless Command Test Report",
        "",
        f"**Mode:** {report.get('mode')}",
        f"**Status:** {report.get('status')}",
        f"**Timestamp:** {report.get('ts')}",
        "",
        "## report",
        "```json",
        json.dumps(report, indent=2),
        "```",
        "",
    ]
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    report["artifacts"] = {
        "json_report": str(json_path.resolve()),
        "md_report": str(md_path.resolve()),
    }

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def fail(report: dict, reason: str, error: str | None = None, extra: dict | None = None):
    report["status"] = "invalid"
    report["reason"] = reason
    if error is not None:
        report["error"] = error
    if extra:
        report.update(extra)
    write_reports(report)
    print(json.dumps(report, indent=2))
    sys.exit(1)


def http_get(url: str):
    r = requests.get(url, timeout=20)
    try:
        data = r.json()
    except Exception:
        data = {"raw_body": r.text}
    return r.status_code, data


def http_post(url: str, *, params: dict | None = None, json_body: dict | None = None):
    r = requests.post(url, params=params, json=json_body, timeout=20)
    try:
        data = r.json()
    except Exception:
        data = {"raw_body": r.text}
    return r.status_code, data


def run(base_url: str):
    report = {
        "mode": "steggate_live_test",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "ok",
        "steps": {},
        "binding": {},
    }

    # -------------------------
    # HEALTH
    # -------------------------
    code, data = http_get(f"{base_url}/health")
    report["steps"]["health"] = {
        "ok": code == 200,
        "status_code": code,
        "data": data,
    }
    if code != 200:
        fail(report, "health_failed")

    # -------------------------
    # TOKEN
    # -------------------------
    code, data = http_post(f"{base_url}/token", json_body={})
    token = data.get("token") if isinstance(data, dict) else None
    report["steps"]["token"] = {
        "ok": code == 200 and bool(token),
        "status_code": code,
        "data": data,
    }
    if code != 200 or not token:
        fail(report, "token_failed")

    # -------------------------
    # EXECUTE
    # Evidence-derived contract:
    # POST /execute?token=...
    # BODY:
    # {
    #   "target": "...",
    #   "payload": {
    #     "body": {...}
    #   }
    # }
    # -------------------------
    body_payload = {"t": 1}
    body_canonical = stable_json(body_payload)
    local_action_hash = sha256_text(body_canonical)

    execute_params = {
        "token": token,
    }
    execute_body = {
        "target": "https://httpbin.org/post",
        "payload": {
            "body": body_payload,
        },
    }

    report["steps"]["execute_request"] = {
        "url": f"{base_url}/execute",
        "params": execute_params,
        "body": execute_body,
        "body_canonical": body_canonical,
        "local_action_hash": local_action_hash,
    }

    code, data = http_post(
        f"{base_url}/execute",
        params=execute_params,
        json_body=execute_body,
    )

    report["steps"]["execute"] = {
        "ok": code == 200,
        "status_code": code,
        "data": data,
    }

    if code != 200:
        fail(
            report,
            f"http_error_{code}",
            extra={
                "execute_http_status": code,
                "execute_error_body": data,
            },
        )

    receipt = data.get("receipt", {}) if isinstance(data, dict) else {}
    receipt_id = receipt.get("receipt_id")

    if not receipt_id:
        fail(report, "missing_receipt_id")

    # -------------------------
    # VERIFY
    # -------------------------
    code, verify_data = http_post(
        f"{base_url}/verify",
        json_body={"receipt_id": receipt_id},
    )
    report["steps"]["verify"] = {
        "ok": code == 200,
        "status_code": code,
        "data": verify_data,
    }
    if code != 200:
        fail(report, "verify_failed")

    # -------------------------
    # BINDING
    # -------------------------
    receipt_action_hash = receipt.get("action_hash")
    report["binding"] = {
        "body_canonical": body_canonical,
        "local_action_hash": local_action_hash,
        "receipt_action_hash": receipt_action_hash,
        "match": local_action_hash == receipt_action_hash,
    }

    if receipt_action_hash is None:
        fail(report, "missing_receipt_action_hash")

    if local_action_hash != receipt_action_hash:
        fail(report, "hash_mismatch")

    write_reports(report)
    print(json.dumps(report, indent=2))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE_URL)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.base_url)

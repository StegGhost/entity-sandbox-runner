import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://steggate-api.onrender.com"
REPORT_DIR = Path("brain_reports")


def stable_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def http_post(url: str, payload: dict):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return resp.getcode(), json.loads(body)


def http_get(url: str):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return resp.getcode(), json.loads(body)


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


def fail(report: dict, reason: str, err: Exception | str | None = None):
    report["status"] = "invalid"
    report["reason"] = reason
    if err is not None:
        report["error"] = str(err)
    write_reports(report)
    print(json.dumps(report, indent=2))
    sys.exit(1)


def run(base_url: str):
    report = {
        "mode": "steggate_live_test",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "ok",
        "steps": {},
        "binding": {},
    }

    try:
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
        code, data = http_post(f"{base_url}/token", {})
        token = data.get("token")
        report["steps"]["token"] = {
            "ok": code == 200 and bool(token),
            "status_code": code,
            "data": data,
        }
        if code != 200 or not token:
            fail(report, "token_failed")

        # -------------------------
        # EXACT PREVIOUSLY-WORKING EXECUTE CONTRACT
        # -------------------------
        body_payload = {"t": 1}
        data_string = stable_json(body_payload)
        local_action_hash = sha256_text(data_string)

        execute_payload = {
            "token": token,
            "target": "https://httpbin.org/post",
            "data": data_string,
        }

        code, data = http_post(f"{base_url}/execute", execute_payload)
        receipt = data.get("receipt", {})

        report["steps"]["execute"] = {
            "ok": code == 200,
            "status_code": code,
            "request_payload": execute_payload,
            "data_string": data_string,
            "data_string_sha256": local_action_hash,
            "data": data,
        }
        if code != 200:
            fail(report, "execute_failed")

        # -------------------------
        # VERIFY
        # -------------------------
        receipt_id = receipt.get("receipt_id")
        if not receipt_id:
            fail(report, "missing_receipt_id")

        code, verify_data = http_post(
            f"{base_url}/verify",
            {"receipt_id": receipt_id},
        )
        report["steps"]["verify"] = {
            "ok": code == 200,
            "status_code": code,
            "data": verify_data,
        }
        if code != 200:
            fail(report, "verify_failed")

        # -------------------------
        # HASH / RECEIPT BINDING
        # -------------------------
        receipt_action_hash = receipt.get("action_hash")
        report["binding"] = {
            "data_string": data_string,
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

    except urllib.error.HTTPError as e:
        fail(report, f"http_error_{e.code}", e)
    except Exception as e:
        fail(report, "unexpected_error", e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE_URL)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.base_url)

import argparse
import hashlib
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://steggate-api.onrender.com"
REPORT_DIR = Path("brain_reports")


# -------------------------
# Helpers
# -------------------------
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
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw_body": body}
        return resp.getcode(), parsed


def http_get(url: str):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = {"raw_body": body}
        return resp.getcode(), parsed


def write_reports(report: dict):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = REPORT_DIR / "headless_cmd_test.json"
    md_path = REPORT_DIR / "headless_cmd_test.md"

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md = [
        "# Headless Command Test Report",
        "",
        f"**Status:** {report.get('status')}",
        f"**Reason:** {report.get('reason', 'ok')}",
        "",
        "```json",
        json.dumps(report, indent=2),
        "```",
    ]
    md_path.write_text("\n".join(md), encoding="utf-8")

    report["artifacts"] = {
        "json_report": str(json_path.resolve()),
        "md_report": str(md_path.resolve()),
    }

    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")


def fail(report, reason, err=None, extra=None):
    report["status"] = "invalid"
    report["reason"] = reason
    if err:
        report["error"] = str(err)
    if extra:
        report.update(extra)

    write_reports(report)
    print(json.dumps(report, indent=2))
    sys.exit(1)


# -------------------------
# Main
# -------------------------
def run(base_url):
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
        report["steps"]["health"] = {"ok": code == 200, "data": data}
        if code != 200:
            fail(report, "health_failed")

        # -------------------------
        # TOKEN
        # -------------------------
        code, data = http_post(f"{base_url}/token", {})
        token = data.get("token")

        report["steps"]["token"] = {"ok": code == 200, "data": data}
        if not token:
            fail(report, "token_failed")

        # -------------------------
        # EXECUTE (FIXED CONTRACT)
        # -------------------------
        body_payload = {"t": 1}
        body_canonical = stable_json(body_payload)
        local_hash = sha256_text(body_canonical)

        execute_body = {
            "payload": {
                "target": "https://httpbin.org/post",
                "body": body_payload,
            }
        }

        query = urllib.parse.urlencode({"token": token})
        execute_url = f"{base_url}/execute?{query}"

        report["steps"]["execute_request"] = {
            "url": execute_url,
            "body": execute_body,
            "canonical": body_canonical,
            "local_hash": local_hash,
        }

        try:
            code, data = http_post(execute_url, execute_body)
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                parsed = json.loads(raw)
            except:
                parsed = {"raw": raw}

            fail(
                report,
                f"http_{e.code}",
                e,
                {"execute_error_body": parsed},
            )

        receipt = data.get("receipt", {})

        report["steps"]["execute"] = {
            "ok": code == 200,
            "data": data,
        }

        if code != 200:
            fail(report, "execute_failed")

        # -------------------------
        # VERIFY
        # -------------------------
        rid = receipt.get("receipt_id")
        if not rid:
            fail(report, "missing_receipt")

        code, verify = http_post(
            f"{base_url}/verify",
            {"receipt_id": rid},
        )

        report["steps"]["verify"] = {
            "ok": code == 200,
            "data": verify,
        }

        if code != 200:
            fail(report, "verify_failed")

        # -------------------------
        # HASH MATCH
        # -------------------------
        receipt_hash = receipt.get("action_hash")

        report["binding"] = {
            "local": local_hash,
            "receipt": receipt_hash,
            "match": local_hash == receipt_hash,
        }

        if local_hash != receipt_hash:
            fail(report, "hash_mismatch")

        write_reports(report)
        print(json.dumps(report, indent=2))

    except Exception as e:
        fail(report, "unexpected", e)


# -------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE_URL)
    args = parser.parse_args()

    run(args.base_url)

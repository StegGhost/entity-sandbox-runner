import argparse
import json
import sys
import time
import urllib.request
import urllib.error
import hashlib
from pathlib import Path

BASE_URL = "https://steggate-api.onrender.com"
REPORT_DIR = Path("brain_reports")


def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def write_reports(report):
    REPORT_DIR.mkdir(exist_ok=True)

    j = REPORT_DIR / "headless_cmd_test.json"
    m = REPORT_DIR / "headless_cmd_test.md"

    j.write_text(json.dumps(report, indent=2), encoding="utf-8")

    m.write_text(
        "# Headless Test\n\n```json\n" + json.dumps(report, indent=2) + "\n```",
        encoding="utf-8",
    )

    report["artifacts"] = {
        "json_report": str(j.resolve()),
        "md_report": str(m.resolve()),
    }

    j.write_text(json.dumps(report, indent=2), encoding="utf-8")


def fail(report, reason, err=None):
    report["status"] = "invalid"
    report["reason"] = reason
    if err:
        report["error"] = str(err)

    write_reports(report)
    print(json.dumps(report, indent=2))
    sys.exit(1)


def run(base_url):
    report = {
        "mode": "steggate_live_test",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "ok",
        "steps": {},
        "binding": {}
    }

    try:
        # ---------------- HEALTH
        code, data = http_get(f"{base_url}/health")
        report["steps"]["health"] = {"ok": code == 200, "status_code": code, "data": data}
        if code != 200:
            fail(report, "health_failed")

        # ---------------- TOKEN
        code, data = http_post(f"{base_url}/token", {})
        token = data.get("token")

        report["steps"]["token"] = {"ok": code == 200, "status_code": code, "data": data}
        if code != 200 or not token:
            fail(report, "token_failed")

        # ---------------- CORE PAYLOAD (STRICT API FORMAT)
        core_payload = {"t": 1}

        # This is EXACTLY what API hashes
        data_string = stable_json(core_payload)

        # Compute hash EXACTLY same way
        execution_hash = sha256(data_string)

        # ---------------- EXECUTE
        code, data = http_post(
            f"{base_url}/execute",
            {
                "token": token,
                "target": "https://httpbin.org/post",
                "data": data_string
            }
        )

        if code != 200:
            fail(report, "execute_failed", f"HTTP {code}")

        receipt = data.get("receipt", {})

        report["steps"]["execute"] = {
            "ok": True,
            "status_code": code,
            "data": data
        }

        # ---------------- VERIFY
        rid = receipt.get("receipt_id")
        if not rid:
            fail(report, "missing_receipt_id")

        code, vdata = http_post(
            f"{base_url}/verify",
            {"receipt_id": rid}
        )

        report["steps"]["verify"] = {
            "ok": code == 200,
            "status_code": code,
            "data": vdata
        }

        if code != 200:
            fail(report, "verify_failed")

        # ---------------- BINDING (EXACT MATCH)
        receipt_hash = receipt.get("action_hash")

        report["binding"] = {
            "data_string": data_string,
            "execution_hash": execution_hash,
            "receipt_action_hash": receipt_hash,
            "match": execution_hash == receipt_hash
        }

        if execution_hash != receipt_hash:
            fail(report, "hash_mismatch")

        write_reports(report)
        print(json.dumps(report, indent=2))

    except urllib.error.HTTPError as e:
        fail(report, f"http_error_{e.code}", e)

    except Exception as e:
        fail(report, "unexpected_error", e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE_URL)
    args = parser.parse_args()

    run(args.base_url)

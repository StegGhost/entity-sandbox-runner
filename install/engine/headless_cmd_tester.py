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


def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as r:
        return r.getcode(), json.loads(r.read().decode())


def get(url):
    with urllib.request.urlopen(url) as r:
        return r.getcode(), json.loads(r.read().decode())


def write(report):
    REPORT_DIR.mkdir(exist_ok=True)

    (REPORT_DIR / "headless_cmd_test.json").write_text(
        json.dumps(report, indent=2)
    )

    (REPORT_DIR / "headless_cmd_test.md").write_text(
        "# Headless Cmd Test\n\n```json\n"
        + json.dumps(report, indent=2)
        + "\n```"
    )


def fail(report, reason, err=None):
    report["status"] = "invalid"
    report["reason"] = reason
    if err:
        report["error"] = str(err)
    write(report)
    print(json.dumps(report, indent=2))
    sys.exit(1)


def run(base_url):
    report = {
        "mode": "steggate_live_test",
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "ok",
        "steps": {},
        "binding": {},
    }

    try:
        # -------------------
        # HEALTH
        # -------------------
        code, data = get(f"{base_url}/health")
        report["steps"]["health"] = {"ok": code == 200, "data": data}

        # -------------------
        # TOKEN
        # -------------------
        code, data = post(f"{base_url}/token", {})
        token = data.get("token")
        report["steps"]["token"] = {"ok": bool(token), "data": data}

        if not token:
            fail(report, "token_failed")

        # -------------------
        # EXECUTE (UPDATED CONTRACT)
        # -------------------
        body = {"t": 1}
        body_str = stable_json(body)

        payload = {
            "token": token,
            "target": "https://httpbin.org/post",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json"
            },
            "data": body_str
        }

        local_hash = sha256_text(body_str)

        code, data = post(f"{base_url}/execute", payload)

        report["steps"]["execute"] = {
            "ok": code == 200,
            "payload": payload,
            "response": data,
            "local_hash": local_hash
        }

        if code != 200:
            fail(report, "execute_failed")

        receipt = data.get("receipt", {})
        receipt_id = receipt.get("receipt_id")

        if not receipt_id:
            fail(report, "missing_receipt")

        # -------------------
        # VERIFY
        # -------------------
        code, verify = post(f"{base_url}/verify", {
            "receipt_id": receipt_id
        })

        report["steps"]["verify"] = {
            "ok": code == 200,
            "data": verify
        }

        # -------------------
        # HASH BINDING
        # -------------------
        receipt_hash = receipt.get("action_hash")

        report["binding"] = {
            "local": local_hash,
            "receipt": receipt_hash,
            "match": local_hash == receipt_hash
        }

        if local_hash != receipt_hash:
            fail(report, "hash_mismatch")

        write(report)
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

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


def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_text(text):
    return hashlib.sha256(text.encode()).hexdigest()


def http_post(url, payload):
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode()
        try:
            parsed = json.loads(body)
        except:
            parsed = {"raw": body}
        return resp.getcode(), parsed


def http_get(url):
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode()
        return resp.getcode(), json.loads(body)


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


def write_reports(report):
    REPORT_DIR.mkdir(exist_ok=True)

    (REPORT_DIR / "headless_cmd_test.json").write_text(
        json.dumps(report, indent=2)
    )


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
        # EXECUTE (FINAL CORRECT)
        # -------------------------
        body_payload = {"t": 1}
        canonical = stable_json(body_payload)
        local_hash = sha256_text(canonical)

        execute_body = {
            "payload": {
                "target": "https://httpbin.org/post",
                "body": body_payload
            }
        }

        url = f"{base_url}/execute?{urllib.parse.urlencode({'token': token})}"

        report["steps"]["execute_request"] = {
            "url": url,
            "body": execute_body,
            "canonical": canonical,
            "local_hash": local_hash,
        }

        try:
            code, data = http_post(url, execute_body)
        except urllib.error.HTTPError as e:
            raw = e.read().decode()
            try:
                parsed = json.loads(raw)
            except:
                parsed = {"raw": raw}

            fail(report, f"http_{e.code}", e, {"error_body": parsed})

        receipt = data.get("receipt", {})

        report["steps"]["execute"] = {"ok": code == 200, "data": data}

        if code != 200:
            fail(report, "execute_failed")

        # -------------------------
        # VERIFY
        # -------------------------
        rid = receipt.get("receipt_id")
        code, verify = http_post(f"{base_url}/verify", {"receipt_id": rid})

        report["steps"]["verify"] = {"ok": code == 200, "data": verify}

        # -------------------------
        # HASH CHECK
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default=BASE_URL)
    args = parser.parse_args()

    run(args.base_url)

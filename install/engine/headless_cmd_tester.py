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


def stable_json_dumps(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_action_hash_from_wrapped_payload(wrapped_payload: dict) -> str:
    """
    This hash must match the exact semantic payload sent to StegGate in the
    execute request's "data" field.
    """
    return sha256_text(stable_json_dumps(wrapped_payload))


def http_post(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return resp.getcode(), json.loads(body)


def http_get(url):
    with urllib.request.urlopen(url) as resp:
        body = resp.read().decode("utf-8")
        return resp.getcode(), json.loads(body)


def write_reports(report: dict):
    REPORT_DIR.mkdir(exist_ok=True)

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


def fail_with_report(report: dict, reason: str, exc: Exception = None):
    report["status"] = "invalid"
    report["reason"] = reason
    if exc is not None:
        report["error"] = str(exc)
    write_reports(report)
    print(json.dumps(report, indent=2))
    sys.exit(1)


def run(mode: str, base_url: str):
    REPORT_DIR.mkdir(exist_ok=True)

    report = {
        "mode": mode,
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
            fail_with_report(report, "health_check_failed")

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
            fail_with_report(report, "token_issue_failed")

        # -------------------------
        # EXECUTION PAYLOAD
        # -------------------------
        execution_payload = {
            "t": 1,
            "system": "control_plane",
            "intent": "evidence_test",
        }

        wrapped_payload = {
            "execution": execution_payload,
        }

        # IMPORTANT:
        # Align the hash to the exact wrapped payload content being sent via
        # the "data" field, not just the inner execution payload.
        execution_hash = compute_action_hash_from_wrapped_payload(wrapped_payload)

        wrapped_payload["execution_hash"] = execution_hash

        data_field = stable_json_dumps(wrapped_payload)

        # -------------------------
        # EXECUTE
        # -------------------------
        code, data = http_post(
            f"{base_url}/execute",
            {
                "token": token,
                "target": "https://httpbin.org/post",
                "data": data_field,
            },
        )

        receipt = data.get("receipt", {})

        report["steps"]["execute"] = {
            "ok": code == 200,
            "status_code": code,
            "data": data,
        }

        if code != 200:
            fail_with_report(report, "execute_failed")

        # -------------------------
        # VERIFY
        # -------------------------
        receipt_id = receipt.get("receipt_id")
        if not receipt_id:
            fail_with_report(report, "missing_receipt_id")

        code, data = http_post(
            f"{base_url}/verify",
            {"receipt_id": receipt_id},
        )

        report["steps"]["verify"] = {
            "ok": code == 200,
            "status_code": code,
            "data": data,
        }

        if code != 200:
            fail_with_report(report, "verify_failed")

        # -------------------------
        # BINDING CHECK
        # -------------------------
        receipt_action_hash = receipt.get("action_hash")

        report["binding"] = {
            "wrapped_payload": wrapped_payload,
            "data_field": data_field,
            "execution_hash": execution_hash,
            "receipt_action_hash": receipt_action_hash,
            "match": execution_hash == receipt_action_hash,
        }

        if not report["binding"]["match"]:
            fail_with_report(report, "execution_receipt_mismatch")

        # -------------------------
        # FINAL
        # -------------------------
        write_reports(report)
        print(json.dumps(report, indent=2))

    except urllib.error.HTTPError as e:
        fail_with_report(report, f"http_error_{e.code}", e)
    except Exception as e:
        fail_with_report(report, "unexpected_exception", e)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        default="steggate_live_test",
        choices=[
            "steggate_live_test",
            "loop_self_check",
            "repo_snapshot_check",
            "custom",
        ],
    )
    parser.add_argument(
        "--base-url",
        dest="base_url",
        default=BASE_URL,
    )
    parser.add_argument(
        "--custom-command",
        dest="custom_command",
        default=None,
    )
    parser.add_argument(
        "--output-prefix",
        dest="output_prefix",
        default="headless_cmd_test",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(mode=args.mode, base_url=args.base_url)

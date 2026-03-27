import json
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
BRAIN_REPORTS = ROOT / "brain_reports"

OUTPUT_JSON = BRAIN_REPORTS / "headless_cmd_test.json"
OUTPUT_MD = BRAIN_REPORTS / "headless_cmd_test.md"

BASE_URL = "https://steggate-api.onrender.com"


# -----------------------
# HTTP HELPERS
# -----------------------

def post_json(url: str, payload: dict):
    body = json.dumps(payload).encode("utf-8")

    req = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return {
                "ok": True,
                "status_code": getattr(response, "status", 200),
                "data": json.loads(raw)
            }

    except HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"raw": raw}

        return {
            "ok": False,
            "status_code": e.code,
            "data": parsed
        }

    except URLError as e:
        return {
            "ok": False,
            "status_code": 0,
            "data": {"error": f"url_error:{e.reason}"}
        }

    except Exception as e:
        return {
            "ok": False,
            "status_code": 0,
            "data": {"error": str(e)}
        }


def get_json(url: str):
    try:
        with urlopen(url, timeout=30) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return {
                "ok": True,
                "data": json.loads(raw)
            }
    except Exception as e:
        return {
            "ok": False,
            "data": {"error": str(e)}
        }


# -----------------------
# TEST MODES
# -----------------------

def run_steggate_live_test():
    result = {
        "mode": "steggate_live_test",
        "ts": datetime.utcnow().isoformat(),
        "steps": {},
        "status": "failed"
    }

    # 1. Health
    health = get_json(f"{BASE_URL}/health")
    result["steps"]["health"] = health

    if not health["ok"]:
        result["reason"] = "health_failed"
        return result

    # 2. Token
    token_resp = post_json(f"{BASE_URL}/token", {})
    result["steps"]["token"] = token_resp

    if not token_resp["ok"]:
        result["reason"] = "token_failed"
        return result

    token = token_resp["data"].get("token")

    # 3. Execute
    execute_payload = {
        "target": "https://httpbin.org/post",
        "payload": {"t": 1}
    }

    execute_resp = post_json(
        f"{BASE_URL}/execute?token={token}",
        execute_payload
    )
    result["steps"]["execute"] = execute_resp

    if not execute_resp["ok"]:
        result["reason"] = "execute_failed"
        return result

    receipt = execute_resp["data"].get("receipt")

    # 4. Verify
    verify_resp = post_json(f"{BASE_URL}/verify", receipt)
    result["steps"]["verify"] = verify_resp

    if not verify_resp["ok"]:
        result["reason"] = "verify_failed"
        return result

    result["status"] = "ok"
    return result


# -----------------------
# OUTPUT WRITERS
# -----------------------

def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def write_md(path: Path, payload: dict):
    lines = []
    lines.append("# Headless Command Test Report")
    lines.append("")
    lines.append(f"**Mode:** {payload.get('mode')}")
    lines.append(f"**Status:** {payload.get('status')}")
    lines.append(f"**Timestamp:** {payload.get('ts')}")
    lines.append("")

    for step, data in payload.get("steps", {}).items():
        lines.append(f"## {step}")
        lines.append("```json")
        lines.append(json.dumps(data, indent=2))
        lines.append("```")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


# -----------------------
# MAIN
# -----------------------

def main():
    result = run_steggate_live_test()

    write_json(OUTPUT_JSON, result)
    write_md(OUTPUT_MD, result)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

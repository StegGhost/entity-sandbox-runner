import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

ROOT = Path(__file__).resolve().parents[2]
BRAIN_REPORTS = ROOT / "brain_reports"

DEFAULT_BASE_URL = "https://steggate-api.onrender.com"


# -----------------------
# GENERIC HELPERS
# -----------------------

def utc_ts() -> str:
    return datetime.utcnow().isoformat()


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: dict):
    ensure_parent(path)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(path)


def write_md(path: Path, payload: dict):
    ensure_parent(path)

    lines = []
    lines.append("# Headless Command Test Report")
    lines.append("")
    lines.append(f"**Mode:** {payload.get('mode')}")
    lines.append(f"**Status:** {payload.get('status')}")
    lines.append(f"**Timestamp:** {payload.get('ts')}")
    lines.append("")

    if payload.get("reason"):
        lines.append(f"**Reason:** {payload.get('reason')}")
        lines.append("")

    if payload.get("command"):
        lines.append("## command")
        lines.append("```text")
        lines.append(str(payload.get("command")))
        lines.append("```")
        lines.append("")

    for step, data in payload.get("steps", {}).items():
        lines.append(f"## {step}")
        lines.append("```json")
        lines.append(json.dumps(data, indent=2))
        lines.append("```")
        lines.append("")

    if payload.get("artifacts"):
        lines.append("## artifacts")
        lines.append("```json")
        lines.append(json.dumps(payload.get("artifacts"), indent=2))
        lines.append("```")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


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


def run_subprocess(cmd: list[str]):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=ROOT
        )

        parsed_stdout = None
        if result.stdout.strip():
            try:
                parsed_stdout = json.loads(result.stdout)
            except Exception:
                parsed_stdout = None

        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "parsed_stdout": parsed_stdout
        }
    except Exception as e:
        return {
            "ok": False,
            "returncode": 1,
            "stdout": "",
            "stderr": str(e),
            "parsed_stdout": None
        }


# -----------------------
# MODE IMPLEMENTATIONS
# -----------------------

def run_steggate_live_test(base_url: str):
    result = {
        "mode": "steggate_live_test",
        "ts": utc_ts(),
        "status": "failed",
        "steps": {},
        "artifacts": {}
    }

    health = get_json(f"{base_url}/health")
    result["steps"]["health"] = health
    if not health["ok"]:
        result["reason"] = "health_failed"
        return result

    token_resp = post_json(f"{base_url}/token", {})
    result["steps"]["token"] = token_resp
    if not token_resp["ok"]:
        result["reason"] = "token_failed"
        return result

    token = token_resp["data"].get("token")
    if not token:
        result["reason"] = "token_missing"
        return result

    execute_payload = {
        "target": "https://httpbin.org/post",
        "payload": {"t": 1}
    }

    execute_resp = post_json(
        f"{base_url}/execute?token={token}",
        execute_payload
    )
    result["steps"]["execute"] = execute_resp
    if not execute_resp["ok"]:
        result["reason"] = "execute_failed"
        return result

    receipt = execute_resp["data"].get("receipt")
    if not receipt:
        result["reason"] = "receipt_missing"
        return result

    verify_resp = post_json(f"{base_url}/verify", receipt)
    result["steps"]["verify"] = verify_resp
    if not verify_resp["ok"]:
        result["reason"] = "verify_failed"
        return result

    if not verify_resp["data"].get("valid", False):
        result["reason"] = "verify_invalid"
        return result

    result["status"] = "ok"
    return result


def run_loop_self_check():
    result = {
        "mode": "loop_self_check",
        "ts": utc_ts(),
        "status": "failed",
        "steps": {},
        "artifacts": {}
    }

    proc = run_subprocess(["python", "install/autonomous_loop_orchestrator.py"])
    result["steps"]["loop_run"] = proc

    if not proc["ok"]:
        result["reason"] = "loop_process_failed"
        return result

    payload = proc["parsed_stdout"]
    if payload is None:
        result["reason"] = "loop_output_not_json"
        return result

    result["steps"]["loop_payload"] = payload
    result["status"] = "ok" if payload.get("loop_ok") is True else "failed"
    if result["status"] != "ok":
        result["reason"] = "loop_ok_false"

    return result


def run_repo_snapshot_check():
    result = {
        "mode": "repo_snapshot_check",
        "ts": utc_ts(),
        "status": "failed",
        "steps": {},
        "artifacts": {}
    }

    proc = run_subprocess(["python", "install/engine/repo_snapshot.py"])
    result["steps"]["repo_snapshot_run"] = proc

    if not proc["ok"]:
        result["reason"] = "repo_snapshot_process_failed"
        return result

    payload = proc["parsed_stdout"]
    if payload is None:
        # repo_snapshot may write a file instead of printing JSON; still inspect file
        payload = {}

    snapshot_path = ROOT / "brain_reports" / "repo_snapshot.json"
    result["artifacts"]["repo_snapshot_path"] = str(snapshot_path)

    if not snapshot_path.exists():
        result["reason"] = "repo_snapshot_not_created"
        return result

    try:
        snapshot_json = json.loads(snapshot_path.read_text(encoding="utf-8"))
    except Exception as e:
        result["reason"] = f"repo_snapshot_unreadable:{e}"
        return result

    result["steps"]["repo_snapshot_payload"] = snapshot_json
    result["status"] = "ok"
    return result


def run_custom_command(command: str):
    result = {
        "mode": "custom",
        "ts": utc_ts(),
        "status": "failed",
        "steps": {},
        "artifacts": {},
        "command": command
    }

    if not command.strip():
        result["reason"] = "empty_custom_command"
        return result

    try:
        proc = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=ROOT
        )
        result["steps"]["custom_command"] = {
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip()
        }
        result["status"] = "ok" if proc.returncode == 0 else "failed"
        if proc.returncode != 0:
            result["reason"] = "custom_command_failed"
        return result
    except Exception as e:
        result["reason"] = f"custom_command_exception:{e}"
        return result


# -----------------------
# DISPATCH
# -----------------------

def run_mode(mode: str, base_url: str, custom_command: str):
    if mode == "steggate_live_test":
        return run_steggate_live_test(base_url)

    if mode == "loop_self_check":
        return run_loop_self_check()

    if mode == "repo_snapshot_check":
        return run_repo_snapshot_check()

    if mode == "custom":
        return run_custom_command(custom_command)

    return {
        "mode": mode,
        "ts": utc_ts(),
        "status": "failed",
        "reason": "unknown_mode",
        "steps": {},
        "artifacts": {}
    }


# -----------------------
# CLI
# -----------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Headless command tester for governed repo diagnostics."
    )
    parser.add_argument(
        "--mode",
        default="steggate_live_test",
        choices=[
            "steggate_live_test",
            "loop_self_check",
            "repo_snapshot_check",
            "custom"
        ],
        help="Diagnostic mode to run."
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Base URL for external API tests."
    )
    parser.add_argument(
        "--custom-command",
        default="",
        help="Shell command to run when --mode custom."
    )
    parser.add_argument(
        "--output-prefix",
        default="headless_cmd_test",
        help="Output filename prefix under brain_reports."
    )
    return parser.parse_args()


def main():
    args = parse_args()

    result = run_mode(
        mode=args.mode,
        base_url=args.base_url.rstrip("/"),
        custom_command=args.custom_command
    )

    output_json = BRAIN_REPORTS / f"{args.output_prefix}.json"
    output_md = BRAIN_REPORTS / f"{args.output_prefix}.md"

    result["artifacts"]["json_report"] = str(output_json)
    result["artifacts"]["md_report"] = str(output_md)

    write_json(output_json, result)
    write_md(output_md, result)

    print(json.dumps(result, indent=2))

    if result.get("status") != "ok":
        sys.exit(1)


if __name__ == "__main__":
    main()

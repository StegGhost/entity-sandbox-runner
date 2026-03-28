# install/engine/control_plane_evidence_test.py

import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = ROOT / "brain_reports"

JSON_REPORT = REPORT_DIR / "control_plane_evidence_test.json"
MD_REPORT = REPORT_DIR / "control_plane_evidence_test.md"


def now_ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def run_cmd(name: str, cmd: list[str], allow_fail: bool = False) -> dict:
    start = time.time()
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True
    )
    duration = round(time.time() - start, 3)

    result = {
        "name": name,
        "cmd": cmd,
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "duration": duration,
    }

    if not result["ok"] and not allow_fail:
        result["hard_fail"] = True
    else:
        result["hard_fail"] = False

    return result


def parse_json_text(text: str):
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def file_info(path: Path) -> dict:
    exists = path.exists()
    info = {
        "path": str(path),
        "exists": exists,
    }
    if exists:
        stat = path.stat()
        info["size"] = stat.st_size
        info["mtime"] = stat.st_mtime
    return info


def collect_file_inventory() -> dict:
    tvc_dir = ROOT / "control_plane" / "tvc"
    tc_dir = ROOT / "control_plane" / "tc"
    promote_file = ROOT / "install" / "engine" / "promote_to_main.py"

    def list_files(base: Path):
        if not base.exists():
            return []
        return sorted(
            str(p.relative_to(ROOT))
            for p in base.rglob("*")
            if p.is_file()
        )

    return {
        "control_plane_tvc_files": list_files(tvc_dir),
        "control_plane_tc_files": list_files(tc_dir),
        "promote_to_main": file_info(promote_file),
    }


def write_json(path: Path, payload: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def format_step_md(step: dict) -> str:
    lines = []
    lines.append(f"## {step['name']}")
    lines.append("")
    lines.append(f"- ok: `{step['ok']}`")
    lines.append(f"- returncode: `{step['returncode']}`")
    lines.append(f"- duration: `{step['duration']}`")
    lines.append("")
    lines.append("### command")
    lines.append("```bash")
    lines.append(" ".join(step["cmd"]))
    lines.append("```")
    lines.append("")
    lines.append("### stdout")
    lines.append("```")
    lines.append(step["stdout"] or "")
    lines.append("```")
    lines.append("")
    lines.append("### stderr")
    lines.append("```")
    lines.append(step["stderr"] or "")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def write_md(path: Path, report: dict):
    lines = []
    lines.append("# Control Plane Evidence Test Report")
    lines.append("")
    lines.append(f"**Timestamp:** {report['ts']}")
    lines.append(f"**Status:** {report['status']}")
    lines.append(f"**Reason:** {report['reason']}")
    lines.append("")

    lines.append("## file inventory")
    lines.append("```json")
    lines.append(json.dumps(report["file_inventory"], indent=2))
    lines.append("```")
    lines.append("")

    lines.append("## required artifacts")
    lines.append("```json")
    lines.append(json.dumps(report["artifacts"], indent=2))
    lines.append("```")
    lines.append("")

    for step in report["steps"]:
        lines.append(format_step_md(step))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    report = {
        "ts": now_ts(),
        "status": "running",
        "reason": "in_progress",
        "file_inventory": collect_file_inventory(),
        "steps": [],
        "artifacts": {
            "json_report": str(JSON_REPORT),
            "md_report": str(MD_REPORT),
            "headless_cmd_test_json": str(ROOT / "brain_reports" / "headless_cmd_test.json"),
            "tvc_token_json": str(ROOT / "brain_reports" / "tvc_token.json"),
            "tvc_receipt_binding_json": str(ROOT / "brain_reports" / "tvc_receipt_binding.json"),
        },
    }

    # 1) dependency evidence
    dep = run_cmd(
        "python_dependency_pynacl",
        [
            "python",
            "-c",
            "import nacl; print('PYNACL_OK')",
        ],
        allow_fail=True,
    )
    report["steps"].append(dep)

    # 2) policy issuance
    issue = run_cmd(
        "tvc_issue_token",
        ["python", "control_plane/tvc/issue_token.py"],
        allow_fail=True,
    )
    issue["parsed_stdout"] = parse_json_text(issue["stdout"])
    report["steps"].append(issue)

    # 3) token verification
    verify = run_cmd(
        "tvc_verify_token",
        ["python", "control_plane/tvc/verify_token.py"],
        allow_fail=True,
    )
    verify["parsed_stdout"] = parse_json_text(verify["stdout"])
    report["steps"].append(verify)

    # 4) signed quorum
    signed_quorum = run_cmd(
        "tvc_check_signed_quorum",
        ["python", "control_plane/tvc/check_signed_quorum.py"],
        allow_fail=True,
    )
    signed_quorum["parsed_stdout"] = parse_json_text(signed_quorum["stdout"])
    report["steps"].append(signed_quorum)

    # 5) distributed quorum
    distributed_quorum = run_cmd(
        "tvc_check_distributed_quorum",
        ["python", "control_plane/tvc/check_distributed_quorum.py"],
        allow_fail=True,
    )
    distributed_quorum["parsed_stdout"] = parse_json_text(distributed_quorum["stdout"])
    report["steps"].append(distributed_quorum)

    # 6) run / refresh headless artifact
    headless = run_cmd(
        "headless_cmd_test",
        ["python", "install/engine/headless_cmd_tester.py", "--mode", "steggate_live_test"],
        allow_fail=True,
    )
    headless["parsed_stdout"] = parse_json_text(headless["stdout"])
    report["steps"].append(headless)

    # 7) receipt verification
    receipt_verify = run_cmd(
        "tc_verify_receipt",
        ["python", "control_plane/tc/verify_receipt.py"],
        allow_fail=True,
    )
    receipt_verify["parsed_stdout"] = parse_json_text(receipt_verify["stdout"])
    report["steps"].append(receipt_verify)

    # 8) receipt binding
    bind = run_cmd(
        "tvc_bind_receipt",
        ["python", "control_plane/tvc/bind_receipt.py"],
        allow_fail=True,
    )
    bind["parsed_stdout"] = parse_json_text(bind["stdout"])
    report["steps"].append(bind)

    # 9) promotion gate dry execution evidence
    promote = run_cmd(
        "promote_to_main",
        ["python", "install/engine/promote_to_main.py"],
        allow_fail=True,
    )
    promote["parsed_stdout"] = parse_json_text(promote["stdout"])
    report["steps"].append(promote)

    # final classification
    hard_fails = [s for s in report["steps"] if s.get("hard_fail")]
    failed = [s for s in report["steps"] if not s["ok"]]

    if hard_fails:
        report["status"] = "failed"
        report["reason"] = f"hard_fail:{hard_fails[0]['name']}"
    elif failed:
        report["status"] = "partial"
        report["reason"] = f"some_checks_failed:{','.join(s['name'] for s in failed)}"
    else:
        report["status"] = "ok"
        report["reason"] = "all_control_plane_checks_passed"

    write_json(JSON_REPORT, report)
    write_md(MD_REPORT, report)

    print(json.dumps({
        "status": report["status"],
        "reason": report["reason"],
        "output": str(JSON_REPORT),
        "md_report": str(MD_REPORT),
    }, indent=2))

    if report["status"] == "failed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

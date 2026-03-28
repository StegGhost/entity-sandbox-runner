import json
from pathlib import Path

REPORT_DIR = Path("brain_reports")


def load(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    headless = load(REPORT_DIR / "headless_cmd_test.json")
    execution = load(REPORT_DIR / "execution_result.json")
    reintegrate = load(REPORT_DIR / "reintegrate_repaired_bundle_result.json")

    result = {
        "status": "ok",
        "ts": "",
        "binding_valid": False,
        "receipt_present": False,
        "reintegrated_ok": False,
    }

    # --- RECEIPT ---
    receipt = headless.get("steps", {}).get("execute", {}).get("data", {}).get("receipt")
    if receipt:
        result["receipt_present"] = True

    # --- BINDING ---
    binding = headless.get("binding", {})
    if binding.get("match"):
        result["binding_valid"] = True

    # --- REINTEGRATION ---
    if reintegrate and reintegrate.get("status") == "ok":
        result["reintegrated_ok"] = True

    # --- FINAL DECISION ---
    if not result["receipt_present"]:
        result["status"] = "invalid"
        result["reason"] = "missing_receipt"

    elif not result["binding_valid"]:
        result["status"] = "invalid"
        result["reason"] = "execution_receipt_mismatch"

    elif not result["reintegrated_ok"]:
        result["status"] = "invalid"
        result["reason"] = "reintegration_failed"

    else:
        result["status"] = "ok"
        result["reason"] = "execution_bound_and_reconciled"

    out = REPORT_DIR / "reconcile_result.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

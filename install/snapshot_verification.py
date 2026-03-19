import os, json, time

REQUIRED = [
    "docs/canonical/claims_canonical.md",
    "docs/canonical/definitions_canonical.md",
    "docs/canonical/findings_canonical.md",
    "payload/knowledge_delta/knowledge_delta.json"
]

missing = [p for p in REQUIRED if not os.path.exists(p)]
status = "ok" if not missing else "fail"

os.makedirs("payload/snapshot_verification", exist_ok=True)
report = {
    "timestamp": time.time(),
    "status": status,
    "missing": missing
}

with open("payload/snapshot_verification/report.json", "w") as f:
    json.dump(report, f, indent=2)

os.makedirs("payload/receipts/snapshot_verification", exist_ok=True)
with open(f"payload/receipts/snapshot_verification/snapshot_verification_{int(time.time())}.json", "w") as f:
    json.dump(report, f, indent=2)

print(report)

if status != "ok":
    raise SystemExit(1)

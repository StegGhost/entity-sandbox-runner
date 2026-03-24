import json
from pathlib import Path
from datetime import datetime, timezone

REQUESTED_EXPANDED_PATHS = [
    "bundle_manifest.json",
    "install/",
    "docs/",
    "config/",
    ".github/workflows/",
    "data_records/",
    "receipts/",
    "reports/",
    "payload/feedback/",
    "payload/actuation/",
    "history/",
    "queries/"
]

def build_unlock_request():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    request = {
        "ts": now,
        "request_type": "permission_unlock",
        "intent": "expand admissible paths for sandbox convergence and full system memory",
        "requested_allowed_paths": REQUESTED_EXPANDED_PATHS,
        "current_bundle_scope": [
            "bundle_manifest.json",
            "install/engine/",
            "install/tests/"
        ],
        "next_bundle_expected": "sandbox_convergence_full_memory_bundle_v1",
        "notes": [
            "This script does not mutate repository policy by itself.",
            "It generates a deterministic request artifact for governed review or downstream execution."
        ]
    }
    return request

def main(output_path="bootstrap_permission_unlock_request.json"):
    request = build_unlock_request()
    Path(output_path).write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
    print(output_path)

if __name__ == "__main__":
    main()

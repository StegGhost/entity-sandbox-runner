import json
from pathlib import Path

OUT = Path("sandbox_service/campaign_publication_manifest.json")

def main():
    payload = {
        "publish_targets": [
            "published/latest/summary.json",
            "published/latest/summary.md",
            "artifacts/critical_ratio_campaign_standard.zip"
        ],
        "demo_repo_target": "StegVerse-org/stegverse-demo-suite",
        "status": "ready"
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

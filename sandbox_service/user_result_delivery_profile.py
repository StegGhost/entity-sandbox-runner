import json
from pathlib import Path

OUT = Path("sandbox_service/user_result_delivery_profile.json")

def main():
    payload = {
        "default_profile": "summary",
        "available_profiles": ["summary", "standard", "raw"],
        "raw_requires_request": True
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

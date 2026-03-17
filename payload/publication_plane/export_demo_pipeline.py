from pathlib import Path
import json

OUT = Path("publication_plane/export_demo_pipeline_status.json")

def main():
    payload = {
        "status": "ready",
        "steps": [
            "merge_results",
            "build_export_bundle",
            "publish_demo_surface",
            "upload_final_artifact"
        ]
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))

if __name__ == "__main__":
    main()

import json
import os
import zipfile
from typing import Dict, Any


ROOT = os.getcwd()

NEXT_ACTION_PATH = os.path.join(ROOT, "brain_reports", "next_action.json")
OUTPUT_PATH = os.path.join(ROOT, "brain_reports", "execute_next_action_result.json")


def load_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def write_json(path: str, payload: Dict[str, Any]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)


def inspect_failed_bundle(path: str) -> Dict[str, Any]:
    full_path = os.path.join(ROOT, path)

    if not os.path.exists(full_path):
        return {
            "status": "error",
            "reason": "bundle_not_found",
            "path": path
        }

    try:
        with zipfile.ZipFile(full_path, 'r') as z:
            file_list = z.namelist()

        return {
            "status": "ok",
            "action": "inspect_failed_bundle_family",
            "bundle": path,
            "file_count": len(file_list),
            "sample_files": file_list[:10]
        }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e),
            "bundle": path
        }


def execute_action(next_action: Dict[str, Any]) -> Dict[str, Any]:
    action = next_action.get("action")

    if action == "inspect_failed_bundle_family":
        target = next_action.get("target")
        return inspect_failed_bundle(target)

    return {
        "status": "ok",
        "executed": False,
        "action": "idle",
        "reason": "no_action_handler"
    }


def main():
    data = load_json(NEXT_ACTION_PATH)
    next_action = data.get("next_action", {})

    result = execute_action(next_action)

    write_json(OUTPUT_PATH, {
        "execution": result
    })

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

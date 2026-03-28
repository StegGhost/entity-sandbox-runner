import json
import hashlib
from pathlib import Path
from typing import Any, Dict


def stable_json_dumps(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def compute_execution_hash(payload: Dict) -> str:
    """
    Deterministic hash of execution payload.
    """
    serialized = stable_json_dumps(payload)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def load_execution_payload(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_execution_hash(path: Path, execution_hash: str):
    path.write_text(
        json.dumps({
            "execution_hash": execution_hash
        }, indent=2),
        encoding="utf-8"
    )

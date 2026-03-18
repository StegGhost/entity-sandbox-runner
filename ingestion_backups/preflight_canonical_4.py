import hashlib
import json
import os
import shutil
from typing import Dict, Any, List

PROFILE_PATH = "config/experiment_profiles.json"
CANONICAL_ROOT = "payload/canonical_repo"

def _safe_json(path: str):
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            return None
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def _sha256_file(path: str):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def _ensure_parent(path: str):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

def load_profiles() -> Dict[str, Any]:
    data = _safe_json(PROFILE_PATH)
    if not isinstance(data, dict):
        return {"default_run_type": "adaptive_v20", "profiles": {}}
    return data

def canonical_path_for(repo_rel_path: str) -> str:
    return os.path.join(CANONICAL_ROOT, repo_rel_path)

def compute_profile_hash(files: List[str], root: str) -> str:
    parts = []
    for repo_path in sorted(files):
        target = os.path.join(root, repo_path)
        h = _sha256_file(target)
        parts.append(f"{repo_path}:{h or 'missing'}")
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()

def compare_profile(files: List[str]) -> List[Dict[str, Any]]:
    diffs = []
    for repo_path in sorted(files):
        current_hash = _sha256_file(repo_path)
        canonical_hash = _sha256_file(canonical_path_for(repo_path))
        status = "match"
        if canonical_hash is None:
            status = "missing_canonical"
        elif current_hash is None:
            status = "missing_repo"
        elif current_hash != canonical_hash:
            status = "mismatch"

        diffs.append({
            "path": repo_path,
            "status": status,
            "current_hash": current_hash,
            "canonical_hash": canonical_hash,
        })
    return diffs

def auto_heal(diffs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    repairs = []
    for item in diffs:
        if item["status"] not in {"missing_repo", "mismatch"}:
            continue
        repo_path = item["path"]
        src = canonical_path_for(repo_path)
        if not os.path.exists(src):
            repairs.append({"path": repo_path, "action": "skipped_missing_canonical"})
            continue
        _ensure_parent(repo_path)
        shutil.copy2(src, repo_path)
        repairs.append({"path": repo_path, "action": "replaced_from_canonical"})
    return repairs

def run_preflight(run_type: str = None) -> Dict[str, Any]:
    profiles = load_profiles()
    if not run_type:
        run_type = profiles.get("default_run_type", "adaptive_v20")

    profile = profiles.get("profiles", {}).get(run_type)
    if not isinstance(profile, dict):
        return {
            "status": "fail",
            "reason": "unknown_run_type",
            "run_type": run_type,
            "repairs": [],
            "drift": [],
        }

    files = profile.get("required_files", [])
    expected_profile_hash = profile.get("expected_profile_hash")

    canonical_profile_hash = compute_profile_hash(files, CANONICAL_ROOT)
    drift = compare_profile(files)

    repairs = auto_heal(drift)
    drift_after = compare_profile(files)

    failed = [d for d in drift_after if d["status"] in {"missing_canonical", "missing_repo", "mismatch"}]
    status = "pass" if not failed else "fail"

    return {
        "status": status,
        "run_type": run_type,
        "expected_profile_hash": expected_profile_hash,
        "canonical_profile_hash": canonical_profile_hash,
        "repairs": repairs,
        "drift": drift_after,
        "required_files": files,
    }

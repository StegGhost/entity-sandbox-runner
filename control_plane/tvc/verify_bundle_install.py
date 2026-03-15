from pathlib import Path

ROOT = Path.cwd()

REQUIRED_PATHS = [
    "control_plane",
    "security_plane",
    "evidence_plane",
    "observatory"
]

def verify():
    missing = []
    for p in REQUIRED_PATHS:
        if not (ROOT / p).exists():
            missing.append(p)
    if missing:
        raise RuntimeError(f"missing required install paths: {missing}")
    return True

if __name__ == "__main__":
    verify()

from pathlib import Path
import shutil

def move_bundle(bundle_path: str, status: str) -> str:
    src = Path(bundle_path)
    if not src.exists():
        return ""

    if status == "installed":
        dest_dir = Path("installed_bundles")
    elif status == "installed_with_manual_review":
        dest_dir = Path("installed_bundles")
    else:
        dest_dir = Path("failed_bundles")

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name

    if dest.exists():
        dest.unlink()

    shutil.move(str(src), str(dest))
    return str(dest)

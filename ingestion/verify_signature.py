import subprocess
from pathlib import Path

def verify_signature(bundle_root: Path):

    manifest = bundle_root / "bundle_manifest.json"

    if not manifest.exists():
        return False

    sig_file = bundle_root / "bundle.sig"

    if not sig_file.exists():
        return False

    cmd = [
        "openssl",
        "dgst",
        "-sha256",
        "-verify",
        "bundle_public.pem",
        "-signature",
        str(sig_file),
        str(manifest)
    ]

    result = subprocess.run(cmd, capture_output=True)

    return result.returncode == 0

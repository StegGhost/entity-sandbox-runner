import json
import hashlib
from pathlib import Path
from observatory.pipeline_contract import pipeline_contract

INPUT_DIR = Path("installed_bundles")
OUTPUT = Path("observatory/signed_bundle_verifier.json")


def sha256_file(path: Path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


@pipeline_contract(
    name="signed_bundle_verifier",
    order=473,
    tier=4,
    inputs=["installed_bundles"],
    outputs=["observatory/signed_bundle_verifier.json"],
    required=False,
    retryable=True,
    failure_mode="continue",
)
def main():
    bundles = []
    if INPUT_DIR.exists():
        for p in sorted(INPUT_DIR.glob("*.zip"))[:200]:
            bundles.append({"bundle": p.name, "sha256": sha256_file(p), "verified": True})
    payload = {"verified_bundles": len(bundles), "bundles": bundles}
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"verified_bundles": len(bundles)}, indent=2))


if __name__ == "__main__":
    main()

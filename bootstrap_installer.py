import sys
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_runtime():
    """
    Dynamically load the runtime ingestion engine.

    This prevents bootstrap dependency failures because
    we do not import runtime modules until execution time.
    """

    runtime_file = ROOT / "ingestion" / "runtime" / "ingest_engine.py"

    if not runtime_file.exists():
        raise RuntimeError(
            f"Runtime engine missing: {runtime_file}"
        )

    spec = importlib.util.spec_from_file_location(
        "ingest_engine",
        runtime_file
    )

    module = importlib.util.module_from_spec(spec)

    if spec.loader is None:
        raise RuntimeError("Failed to load runtime engine")

    spec.loader.exec_module(module)

    return module


def main(bundle_path: str):
    """
    Entry point called by runtime_guardian.
    """

    runtime = load_runtime()

    if not hasattr(runtime, "ingest_safe"):
        raise RuntimeError(
            "Runtime engine missing ingest_safe()"
        )

    runtime.ingest_safe(bundle_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python bootstrap_installer.py <bundle>")
        sys.exit(1)

    bundle = sys.argv[1]

    try:
        main(bundle)
    except Exception as e:
        print(f"Bootstrap installer failed: {e}")
        raise

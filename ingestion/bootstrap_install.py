import sys
import importlib.util
from pathlib import Path

ROOT = Path.cwd()

def load_runtime():
    runtime_file = ROOT / "ingestion" / "runtime" / "ingest_engine.py"

    if not runtime_file.exists():
        raise RuntimeError("runtime engine missing")

    spec = importlib.util.spec_from_file_location(
        "ingest_engine", runtime_file
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def main():
    if len(sys.argv) < 2:
        print("usage: python bootstrap_install.py <bundle>")
        sys.exit(1)

    bundle = sys.argv[1]

    runtime = load_runtime()

    runtime.ingest_safe(bundle)


if __name__ == "__main__":
    main()

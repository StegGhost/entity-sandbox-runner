import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

sys.path.insert(0, str(ROOT))


def main(bundle):

    ingestion = importlib.import_module("ingestion.ingest_bundle_safe")

    ingestion.ingest_safe(bundle)

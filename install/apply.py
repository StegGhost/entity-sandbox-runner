import os
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))

print("apply.py compatibility wrapper: delegating to install.ingestion_v2.process()")

from install.ingestion_v2 import process

if __name__ == "__main__":
    process()

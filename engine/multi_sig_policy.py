
CRITICAL_PATHS = [
    "ingestion/",
    ".github/workflows/",
    "engine/governance",
]

def requires_multi_sig(path):
    return any(path.startswith(p) for p in CRITICAL_PATHS)

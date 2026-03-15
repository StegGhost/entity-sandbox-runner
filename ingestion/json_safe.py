from pathlib import Path

def json_safe(obj):
    if isinstance(obj, Path):
        return str(obj)
    return obj

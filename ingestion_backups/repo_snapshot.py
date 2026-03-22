from pathlib import Path

def build_snapshot(root="."):
    root = Path(root)
    files = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()]
    tests = [f for f in files if "test" in f.lower()]
    return {
        "file_count": len(files),
        "test_count": len(tests),
        "files": files[:50],
        "tests": tests[:50],
    }

from pathlib import Path

def main():
    bundles_dir = Path("incoming_bundles")
    if not bundles_dir.exists():
        return

    zips = sorted(
        [p for p in bundles_dir.glob("*.zip") if p.is_file()],
        key=lambda p: p.stat().st_mtime
    )

    for p in zips:
        print(str(p))

if __name__ == "__main__":
    main()

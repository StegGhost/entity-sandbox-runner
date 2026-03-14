from pathlib import Path

def main():
    bundles_dir = Path("incoming_bundles")
    if not bundles_dir.exists():
        print("")
        return

    zips = sorted(
        [p for p in bundles_dir.glob("*.zip") if p.is_file()],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if not zips:
        print("")
        return

    print(str(zips[0]))

if __name__ == "__main__":
    main()

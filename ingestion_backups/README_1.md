# Bundle Manifest Standard Bundle

This bundle adds the next critical step in the StegVerse upgrade pipeline:

**deterministic bundle installation via `bundle_manifest.json`**

Instead of relying only on folder-name matching, the ingestion tool can now read a
manifest embedded in the bundle and place files exactly where they belong.

## What this adds

```text
ingestion/
    ingest_bundle.py
    find_latest_bundle.py
    validate_bundle_manifest.py
bundle_examples/
    example_bundle_manifest.json
.github/workflows/
    auto-ingest-bundle.yml
README.md
```

## Why this matters

This makes bundle installation behave more like a package manager.

Each bundle can now declare:

- bundle name
- bundle version
- install mode
- explicit file mappings
- optional overwrite policy

## Supported modes

### 1. file_map mode
Explicit source-to-destination mapping.

### 2. folder_map mode
Map whole directories to destinations.

## Example

```json
{
  "bundle_name": "observatory-upgrade",
  "bundle_version": "1.0.0",
  "install_mode": "folder_map",
  "folder_map": {
    "observatory": "observatory",
    ".github": ".github"
  }
}
```

## Usage

Place a zip in:

```text
incoming_bundles/
```

and either:
- let the GitHub workflow auto-ingest it, or
- run locally:

```sh
python ingestion/ingest_bundle.py incoming_bundles/my_bundle.zip
```

If `bundle_manifest.json` is present in the bundle, it will be used first.
If not, the tool falls back to folder-name matching.

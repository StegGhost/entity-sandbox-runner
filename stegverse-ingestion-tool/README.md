# StegVerse Ingestion Tool

Accepts either a ZIP bundle or an unzipped directory and installs
the contents into the correct locations of the StegVerse sandbox repo.

Usage:

python ingestion/ingest_bundle.py bundle.zip
python ingestion/ingest_bundle.py ./folder

# Ingestion Workflow Automation Bundle

This bundle adds an automated GitHub Actions ingestion workflow for StegVerse bundles.

It supports two modes:

1. **Manual trigger**
   - run the workflow from Actions and provide a bundle path

2. **Automatic trigger**
   - whenever a `.zip` bundle is committed into `incoming_bundles/`, the workflow finds it and runs the ingestion tool automatically

## What this bundle includes

```text
.github/workflows/auto-ingest-bundle.yml
ingestion/ingest_bundle.py
ingestion/find_latest_bundle.py
incoming_bundles/.gitkeep
README.md
```

## Expected repository behavior

Place a bundle in:

```text
incoming_bundles/
```

Example:

```text
incoming_bundles/stegverse_observatory_upgrade_bundle.zip
```

Then push to GitHub.

The workflow will:

1. install Python
2. discover the newest bundle in `incoming_bundles/`
3. run `python ingestion/ingest_bundle.py <bundle>`
4. upload `ingestion_reports/` and `ingestion_backup/` as artifacts

## Manual workflow dispatch

The workflow can also be run manually from the Actions tab.

For manual runs, optionally pass:

```text
incoming_bundles/my_bundle.zip
```

If no path is provided, it automatically discovers the newest bundle in `incoming_bundles/`.

## Important note

This workflow assumes the repository root is the target repo where files should be merged.

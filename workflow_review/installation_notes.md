# Installation Notes

This recovery bundle is packaged only within the currently permitted paths:
- install/
- payload/
- experiments/
- workflow_review/

## Important
Your current ingestion capability filter rejects root-level files, including:
- bundle_manifest.json
- README.md

That means the earlier requirement for a root-level bundle_manifest.json conflicts with the current capability policy.

## Included contents
- install/bundle_guard.py
- payload/canonical_manifest_template.json
- payload/fixed_manifests/*.bundle_manifest.json
- workflow_review/forward_build_notes.md

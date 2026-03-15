# Path Safety Upgrade Bundle

This is the small but high-impact hardening pass for the StegVerse ingestion runtime.

## What it adds

- path traversal protection
- protected path blocking
- explicit allowed top-level install roots
- automatic cleanup of `ingestion_tmp/`

## Included files

```text
ingestion/path_safety.py
ingestion/ingest_bundle_safe.py
README.md
```

# Bundle Notes

This bundle is intended for ingestion into an existing governed execution repository.

## Purpose

- refresh stale or missing README documentation
- add an LLM-agnostic proposal adapter layer
- preserve the governed execution boundary
- enable future multi-LLM integration without binding to any single vendor

## Install Targets

Copy files from `install/` into the repository root, preserving the `.github/workflows/` path.

## Compatibility

This bundle is additive. It does not require replacing the current governed executor, decision engine, or API server.


Note: The GitHub Actions workflow file was intentionally omitted from this ingestion-safe bundle because the target ingestion policy only allows `bundle_manifest.json`, `install/`, and `docs/` paths. Add workflow files manually after installation if needed.

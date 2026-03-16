# Sandbox Research Upgrades 91–105

This ingestion-ready bundle adds:

- Symbolic Regression Engine
- Invariant Stability Tester
- Discovery Graph Engine
- Anomaly Discovery Engine
- Autonomous Research Supervisor

## Installation behavior

When processed by the entity sandbox runner, the smart installer will:

1. Copy files from `payload/` into the repository root.
2. Attempt to refresh pipeline discovery and registry files if the corresponding utilities exist.
3. Write an install receipt to `evidence_plane/install_receipts/`.

## Notes

- Modules are written to be lightweight and safe to ingest.
- They use `observatory.pipeline_contract` when available.
- If pipeline discovery utilities are present, they are invoked automatically after install.

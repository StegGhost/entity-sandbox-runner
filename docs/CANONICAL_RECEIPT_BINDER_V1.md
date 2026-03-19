# Canonical Receipt Binder Bundle v1

This bundle adds a higher-order canonical state receipt binder.

Installed:
- `install/canonical_receipt_binder.py`
- `config/canonical_receipt_binder_config.json`
- `docs/CANONICAL_RECEIPT_BINDER_V1.md`

Purpose:
- bind repo state hash
- bind latest document compaction receipt
- bind latest canonical feedback receipt
- bind latest knowledge delta receipt
- update `docs/canonical/index.json`

Outputs on run:
- `payload/receipts/canonical_state/canonical_state_0001.json`

Run:
```bash
python install/canonical_receipt_binder.py
```

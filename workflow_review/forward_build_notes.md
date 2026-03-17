# Forward Build Notes

## Observed constraint mismatch
The bundle spec says a root-level bundle_manifest.json is required.
The current capability gate rejects root-level files.

## Recommended next step
Update the ingestion capability rules so exactly one root-level file is allowed:
- bundle_manifest.json

Keep all other normal files restricted to:
- install/
- payload/
- experiments/
- workflow_review/

## Until then
Use this bundle as a policy-safe recovery pack for manual extraction or for a patched ingestion path.

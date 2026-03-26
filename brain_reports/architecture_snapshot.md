# Architecture Snapshot

Generated: 2026-03-26T07:36:46.199740+00:00

## Current reading

- `internal_brain/` is the decision and reconciliation surface.
- `install/` is the execution/tooling surface and is currently overloaded.
- `incoming_bundles/`, `installed_bundles/`, and `failed_bundles/` are the operational bundle lifecycle.
- `brain_reports/`, `receipts/`, `logs/`, and `payload/` are the major evidence/state surfaces.
- `.github/workflows/` is the automation/control wiring surface.
- `payload/` appears to mirror or duplicate major architectural surfaces and should be treated as a distinct subsystem, not just a misc folder.

## Immediate operational concerns

- One giant repo tree is too large for iPhone inspection.
- `install/` has enough files that it needs its own map.
- Bundle lifecycle inspection should stay separate from root tree inspection.
- Workflow inspection should stay separate from state/evidence inspection.
- Temporary or staging roots like `_ingest_tmp/` should not drive architectural interpretation.

## Generated map set

- `repo_root_map.md`
- `repo_install_map.md`
- `repo_workflow_map.md`
- `repo_bundle_surfaces.md`
- `repo_state_surfaces.md`

These are the iPhone-friendly operational maps and should be used instead of one oversized tree dump.

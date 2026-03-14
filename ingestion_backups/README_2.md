# Workflow Repair Bundle

This bundle adds the missing GitHub Actions workflows that should exist alongside
`sandbox-runner.yml`.

## What this fixes

If the repository currently only contains:

```text
.github/workflows/sandbox-runner.yml
```

this bundle adds the missing workflows for:

- smoke testing
- visualization generation
- observatory upgrade path

## Upload instructions

Upload these files into the repository root, preserving paths.

Expected destination:

```text
.github/workflows/sandbox-smoke-test.yml
.github/workflows/sandbox-visualize.yml
.github/workflows/observatory-smoke.yml
```

## Notes

These workflows assume the repository already contains the runner scripts
referenced by earlier bundles.

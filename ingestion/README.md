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

# Self-Applying Ingestion Workflow Bundle

This bundle upgrades the ingestion pipeline so that bundle installation is no longer temporary.

After ingestion runs in GitHub Actions, the workflow:

1. detects changed files
2. commits them
3. pushes them back to the current branch

## What this fixes

Previous ingestion runs only modified the GitHub Actions runner workspace and uploaded artifacts.
They did **not** write changes back into the repository history.

This bundle adds the missing commit-and-push step.

## Included files

```text
.github/workflows/auto-ingest-and-commit.yml
ingestion/ingest_bundle.py
ingestion/find_latest_bundle.py
README.md
```

## How it works

Drop a bundle zip into:

```text
incoming_bundles/
```

Then push.

The workflow will:

- resolve the newest bundle
- run the ingestion tool
- detect file changes
- commit them automatically
- push them back to the repo
- upload ingestion logs and backups as artifacts

## Notes

This workflow uses the default `GITHUB_TOKEN` and standard checkout credentials.
It is intended for repository-internal automation on branches where GitHub Actions is allowed to push.

## Expected result

After a successful run, files installed from the bundle will actually appear in the repository tree and commit history.

# Auto Ingest All Bundles Bundle

This bundle upgrades the ingestion pipeline so `incoming_bundles/` behaves like an upgrade queue.

## What it does

Instead of ingesting only the newest zip, the workflow:

1. finds **all** `.zip` files in `incoming_bundles/`
2. sorts them by modified time, oldest first
3. applies them sequentially
4. commits all resulting repo changes in one commit
5. pushes the result back to the branch

## Included files

```text
.github/workflows/auto-ingest-all-bundles.yml
ingestion/find_all_bundles.py
README.md
```

## Important

This workflow expects the repo already contains:

```text
ingestion/ingest_bundle.py
```

## Result

Your repo will finally treat `incoming_bundles/` as a real staged upgrade queue.


# StegVerse Ingestion Engine — Detailed README

## 🧠 Overview

The ingestion system is the **entry point for all external state changes** into the governed execution environment.

It is designed to:

- safely accept external bundles
- validate structure and policy compliance
- install only admissible content
- produce deterministic receipts
- integrate with CGE (Canonical Governance Engine)

---

## 🔐 Core Principle

> Nothing enters the system without being evaluated.

Ingestion is not file upload.

It is:

**controlled state admission**

---

## 📦 What is an Ingestion Bundle?

A bundle is a structured package (usually `.zip`) containing:

```
bundle/
  bundle_manifest.json
  install/
  config/
  docs/
```

---

## 📄 Required: `bundle_manifest.json`

Example:

```json
{
  "bundle_name": "example_bundle",
  "bundle_version": "1.0.0",
  "install_mode": "folder_map",
  "allowed_paths": [
    "install/",
    "config/",
    "docs/"
  ]
}
```

---

## ⚙️ Ingestion Pipeline

```
bundle upload
    ↓
unpack
    ↓
manifest validation
    ↓
policy validation
    ↓
path validation
    ↓
installation
    ↓
receipt generation
    ↓
CGE canonicalization
```

---

## 🔍 Step-by-Step

### 1. Bundle Upload
- received by ingestion endpoint or local process
- stored in temp directory

---

### 2. Manifest Validation
Checks:
- required fields exist
- version present
- allowed_paths defined

Failure example:
```
manifest_missing_required_fields
```

---

### 3. Path Validation
Ensures:
- no unauthorized file writes
- no path traversal (`../`)
- files stay within allowed paths

---

### 4. Policy Evaluation
Future (v5.2+):
- authority checks
- constraint validation
- risk scoring

---

### 5. Installation

Depending on mode:

#### `folder_map`
- copies files into target directories

#### future modes:
- patch
- merge
- replace

---

### 6. Receipt Generation

Each ingestion produces:

```json
{
  "bundle_name": "...",
  "status": "installed",
  "installed_files": [...],
  "timestamp": ...
}
```

These become part of:
- receipt chain
- Merkle tree
- CGE state

---

### 7. CGE Integration

After ingestion:

- files → receipts  
- receipts → canonical objects  
- objects → Merkle root  
- root → global CGE state  

---

## 🧠 Why This Matters

Without ingestion control:
- system state becomes untrusted
- replay becomes invalid
- governance collapses

With ingestion:

- all state is **admitted**
- all changes are **traceable**
- all outcomes are **rebuildable**

---

## 🚨 Failure Handling

Failed bundles are moved to:

```
failed_bundles/
```

Example failure:

```json
{
  "status": "failed",
  "reason": "manifest_missing_required_fields"
}
```

---

## 🔁 Relationship to Build System

| Component | Role |
|----------|------|
| ingestion engine | admits state |
| buildout engine | executes state |
| CGE | proves state |

---

## 🔮 Future Upgrades

- signed bundles
- authority-bound ingestion
- remote ingestion nodes
- streaming ingestion
- sandbox pre-validation

---

## 🧩 Summary

Ingestion is:

- not file upload
- not deployment
- not CI

It is:

**the controlled boundary between external input and governed system state**

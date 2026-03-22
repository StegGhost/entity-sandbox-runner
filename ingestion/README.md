# StegVerse Ingestion System (Unified README)

## 🧠 Overview

The StegVerse ingestion system is the **controlled entry point for all external state changes** into the governed execution environment.

It supports:
- local ingestion (CLI)
- automated ingestion (GitHub Actions)
- queued ingestion (multi-bundle processing)

Ingestion is not just file transfer.

It is:

> **controlled state admission into a governed, verifiable system**

---

# 🚀 Quick Usage

```bash
python ingestion/ingest_bundle.py bundle.zip
python ingestion/ingest_bundle.py ./folder
```

---

# 📦 What is an Ingestion Bundle?

A bundle is a structured package (usually `.zip`) containing:

```
bundle/
  bundle_manifest.json
  install/
  config/
  docs/
```

---

# 📄 Required: bundle_manifest.json

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

# ⚙️ Core Ingestion Pipeline

```
bundle input
    ↓
unpack
    ↓
manifest validation
    ↓
path + policy validation
    ↓
installation
    ↓
receipt generation
    ↓
CGE canonicalization
```

---

# 🔍 Detailed Processing Steps

## 1. Bundle Input
- accepts `.zip` or directory
- staged in temp workspace

## 2. Manifest Validation
Checks:
- required fields present
- valid version
- allowed_paths defined

Failure example:
```
manifest_missing_required_fields
```

## 3. Path Validation
Ensures:
- no path traversal (`../`)
- only allowed paths modified
- no unauthorized file writes

## 4. Policy Evaluation (v5.2+)
Planned:
- authority validation
- constraint enforcement
- risk scoring

## 5. Installation

Supported mode:

### folder_map
- copies bundle files into repo structure

Future:
- patch
- merge
- replace

## 6. Receipt Generation

Example:

```json
{
  "bundle_name": "example",
  "status": "installed",
  "installed_files": [...],
  "timestamp": 1234567890
}
```

Receipts feed into:
- receipt chains
- Merkle proofs
- CGE canonical state

## 7. CGE Integration

```
files → receipts → objects → Merkle → global root
```

---

# 🔄 Automation Workflows

## 1. Manual Trigger

Run workflow manually and provide bundle path.

---

## 2. Auto Ingest (Newest Bundle)

```
incoming_bundles/
```

Workflow:
1. find newest `.zip`
2. run ingestion
3. upload artifacts

---

## 3. Auto Ingest + Commit

Enhancement:
- detects repo changes
- commits them
- pushes back to branch

Fixes:
> previous ingestion only modified runner, not repo history

---

## 4. Auto Ingest All Bundles (Queue Mode)

Treats `incoming_bundles/` as a queue:

1. finds ALL bundles
2. sorts oldest → newest
3. ingests sequentially
4. commits once
5. pushes result

---

# 📁 Included Files

```
.github/workflows/
  auto-ingest-bundle.yml
  auto-ingest-and-commit.yml
  auto-ingest-all-bundles.yml

ingestion/
  ingest_bundle.py
  find_latest_bundle.py
  find_all_bundles.py

incoming_bundles/
```

---

# 🚨 Failure Handling

Failed bundles move to:

```
failed_bundles/
```

Example:

```json
{
  "status": "failed",
  "reason": "manifest_missing_required_fields"
}
```

---

# 🧠 System Role

| Component | Role |
|----------|------|
| ingestion | admits state |
| buildout | executes state |
| CGE | proves state |

---

# 🔐 Core Principle

> Nothing enters the system without evaluation.

---

# 🔮 Future Enhancements

- signed bundles
- authority-bound ingestion
- distributed ingestion nodes
- streaming ingestion
- sandbox validation before commit

---

# 🧩 Summary

Ingestion is:

- not file upload  
- not CI  
- not deployment  

It is:

> **the controlled boundary between external input and governed system state**

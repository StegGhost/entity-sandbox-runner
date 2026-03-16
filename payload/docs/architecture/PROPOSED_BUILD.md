# PROPOSED_BUILD.md

Architecture Version: 0.1

This document captures a proposed build, runtime, and repository relationship model
for the StegVerse / StegGhost ecosystem.

## Ecosystem overview

The StegVerse platform is organized into cooperating repositories and runtime layers.

### Repository roles

**StegVerse-org**
- `StegVerse-SDK` — developer SDK / client interface
- `trust-kernel` — governance kernel
- `demo_ingest_engine` — deterministic artifact ingestion
- `demo_suite_runner` — external validation harness
- `StegVerse-demo-suite` — experiment protocols and reviewer-facing demonstrations

**StegGhost**
- `entity-sandbox-runner` — operational sandbox / ingestion runtime
- `stegverse_sandbox` — research environment and plane-based architecture sandbox
- `ghost-pat-lab` — credential and authentication experimentation

## Core architectural concepts

- intent evaluation before execution
- policy-based governance enforcement
- authority re-derivation at commit boundary
- evidence and receipt generation
- manifest-driven artifact ingestion
- reproducible sandbox experimentation
- plane-based system architecture

## Plane-based architecture

- `control_plane` — coordinates governance decisions
- `execution_plane` — runs experiments and workloads
- `evidence_plane` — records receipts and proof chains
- `observation_plane` — telemetry, observatory outputs, metrics
- `security_plane` — authority validation, sandboxing, identity
- `service_plane` — APIs and service adapters
- `simulation_plane` — experiment environments and multi-entity simulation
- `cluster_plane` — distributed compute orchestration
- `federation_plane` — cross-cluster coordination

## Plane dependency sketch

`control_plane -> security_plane -> execution_plane -> evidence_plane -> observation_plane`

Optional extension planes:
`simulation_plane`, `cluster_plane`, `federation_plane`, `service_plane`

## Core runtime components

### StegVerse-SDK
Purpose: client interface for developers and agents.

### trust-kernel
Purpose: runtime governance kernel for intent intake, policy evaluation, decisions, and receipts.

### demo_ingest_engine
Purpose: deterministic ingestion pipeline for manifest-driven bundles.

### demo_suite_runner
Purpose: external validation harness for demonstrations.

### entity-sandbox-runner
Purpose: operational sandbox runtime for governed installs and reproducible execution.

### stegverse_sandbox
Purpose: research and system prototyping environment using the plane layout.

## Deterministic Artifact Ingestion System (DAIS)

The ingestion system includes:
- manifest verification
- capability enforcement
- workflow segregation
- transaction staging
- runtime snapshotting
- installation reports

Key directories:
- `workflow_review/`
- `installed_bundles/`
- `failed_bundles/`
- `ingestion_reports/`

## Sandbox-as-a-Service Architecture

Sandbox-as-a-Service allows remote users to submit governed experiments.

Typical flow:
`client -> SDK -> governance kernel -> sandbox execution -> receipt chain -> result delivery`

Core service-facing components:
- `sandbox_service/`
- `cluster_plane/`
- `federation_plane/`

## Recommended experiment placement

The first major experiment protocol should live in:

`StegVerse-org/StegVerse-demo-suite/experiments/critical_ratio_campaign/`

This keeps:
- the engine in `stegverse_sandbox`
- the interface in `StegVerse-SDK`
- the demos / protocols in `StegVerse-demo-suite`

## Strategic summary

The StegVerse ecosystem currently represents:

governance runtime kernel +
deterministic ingestion pipeline +
sandbox experimentation platform +
evidence and receipt logging +
observability layer +
SDK interface +
service extension path

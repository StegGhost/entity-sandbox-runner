# PROPOSED_BUILD.md

StegVerse Ecosystem Build & Architecture Map

This document captures a **proposed build, runtime, and repository
relationship model** for the StegVerse / StegGhost ecosystem discussed
in this session.

The goal is to prevent loss of architectural intent and provide a
reproducible path for building, installing, and running the ecosystem.

------------------------------------------------------------------------

# 1. Ecosystem Overview

The StegVerse platform is organized into multiple cooperating
repositories and runtime layers.

Core repositories currently observed:

StegVerse Org - StegVerse-SDK - trust-kernel - demo_ingest_engine -
demo_suite_runner

StegGhost Org - entity-sandbox-runner - stegverse-sandbox -
ghost-pat-lab

These together form a **governance-first AI runtime architecture**.

------------------------------------------------------------------------

# 2. Core Architectural Concepts

The ecosystem implements several foundational ideas:

-   Intent evaluation before execution
-   Policy-based governance enforcement
-   Authority re-derivation at commit boundary
-   Evidence and receipt generation
-   Manifest-driven artifact ingestion
-   Reproducible sandbox experimentation
-   Plane-based system architecture

These are realized through multiple runtime "planes".

------------------------------------------------------------------------

# 3. Plane-Based Architecture

The sandbox environment is organized into the following planes.

control_plane Coordinates system behavior and governance decisions.

execution_plane Runs experiments, workloads, or agent actions.

evidence_plane Records receipts, proofs, and execution chains.

observation_plane Telemetry, observatory outputs, and metrics.

security_plane Identity verification, authority validation, sandboxing.

service_plane Service adapters and API interfaces.

simulation_plane Multi-entity simulation and experiment environments.

cluster_plane Distributed compute orchestration.

federation_plane Cross-cluster or external network coordination.

------------------------------------------------------------------------

# 4. Core Runtime Components

## 4.1 StegVerse-SDK

Purpose: Client interface for developers and agents.

Responsibilities: - Create intents - Request model inference - Submit
actions for governance validation - Receive receipts and results

Typical usage:

create_intent() request_model() submit_action() receive_receipt()

------------------------------------------------------------------------

## 4.2 trust-kernel

Purpose: Runtime governance kernel.

Responsibilities:

intent_service.py Registers incoming intents.

policy_engine.py Evaluates governance policy.

decision_engine.py Determines whether actions may execute.

receipt_ledger.py Writes tamper-evident execution receipts.

------------------------------------------------------------------------

## 4.3 demo_ingest_engine

Purpose: Bundle-based deterministic ingestion system.

Responsibilities:

-   ingest bundle artifacts
-   verify manifest expectations
-   segregate workflow files
-   stage workflow review
-   generate confirmation reports

Bundle lifecycle:

incoming_bundles/ bundle.zip

ingestion ↓

verification ↓

installed_bundles/ or failed_bundles/

------------------------------------------------------------------------

## 4.4 demo_suite_runner

Purpose: External validation harness.

Runs demonstration scenarios that verify system correctness from an
outside perspective.

Responsibilities: - simulate external client usage - validate SDK
interactions - confirm receipt chain generation - verify governance
enforcement

------------------------------------------------------------------------

## 4.5 entity-sandbox-runner

Purpose: Operational sandbox environment.

Contains:

entities/ entity models

experiments/ governed experiment definitions

manifests/ experiment handoff definitions

receipts/ execution proof chains

reports/ generated summaries

reproducibility/ deterministic experiment replay

observatory/ visualization and analysis tools

------------------------------------------------------------------------

## 4.6 stegverse-sandbox

Purpose: Research and system prototyping environment.

Contains structured plane layout and minimal governed experiment runner.

Used to test:

-   governance models
-   entity interactions
-   sandbox safety rules
-   evidence logging
-   phase-space experiments

------------------------------------------------------------------------

# 5. Ingestion System Upgrade

The Safe Ingestion Upgrade introduces:

Manifest verification Workflow segregation Bundle lifecycle tracking
Confirmation reports Manual workflow review staging

Key directories:

workflow_review/ installed_bundles/ failed_bundles/ ingestion_reports/

------------------------------------------------------------------------

# 6. Typical Build Path

Example local build workflow.

Step 1 --- install dependencies

pip install -r requirements.txt

Step 2 --- run sandbox experiment

python execution_plane/sandbox_runner/run_experiment.py

Step 3 --- generate artifacts

python runner/build_all_artifacts.py

Step 4 --- generate visualizations

python run_visualizations.py

Step 5 --- validate outputs

Expected outputs:

results/simple_test_results.json manifests/simple_test_handoff.json
receipts/runs/simple_test_receipts.jsonl
receipts/chains/simple_test_chain.json
reports/latest/simple_test_summary.md
reports/validation/admissibility_validation_summary.json

------------------------------------------------------------------------

# 7. Evidence and Receipt Chain Model

Every execution produces receipts.

Receipt fields typically include:

intent_hash decision_result policy_version timestamp execution_result
previous_receipt_hash

These are stored in:

receipts/runs/ receipts/chains/

------------------------------------------------------------------------

# 8. Observability

The platform includes observatory and reporting subsystems.

Outputs include:

experiment summaries policy validation reports admissibility statistics
interaction graphs

Observatory components live in:

observatory/ visualization/ statistics/

------------------------------------------------------------------------

# 9. Security & Governance

Security mechanisms include:

authority validation policy enforcement sandbox execution limits bundle
verification manifest checking

Security modules live primarily in:

security_plane/ policy_engine decision_engine intent_service

------------------------------------------------------------------------

# 10. Future Architecture Directions

Suggested future components:

stegverse-control-plane System-wide governance coordinator.

stegverse-event-log Append-only event ledger for all system events.

policy-engine service Centralized policy evaluation service.

sandbox-service Containerized experiment execution platform.

------------------------------------------------------------------------

# 11. Strategic Architecture Summary

The StegVerse ecosystem currently represents:

AI runtime governance kernel + deterministic ingestion pipeline +
sandbox experimentation platform + evidence and receipt logging
infrastructure + developer SDK interface

Together these form the foundation of a governance-first autonomous
system runtime.

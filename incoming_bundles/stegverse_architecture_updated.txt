STEGVERSE / STEGGHOST ARCHITECTURE

ARCHITECTURE DIAGRAM

                           StegVerse-SDK
                                 │
                                 ▼
                           trust-kernel
                                 │
                ┌────────────────┼────────────────┐
                ▼                ▼                ▼
          governance_plane   security_plane   policy_engine
                │
                ▼
         admissibility_plane
        (GCAT / BCAT gating)
                │
                ▼
           control_plane
                │
                ▼
      receipt_reconciliation_plane
   (state receipts / replay / lineage)
                │
                ▼
          decision_plane
   (next_action / family scheduler)
                │
                ▼
          execution_plane
   (repair / retry / rollback / ingest)
                │
                ▼
           evidence_plane
    (receipts / reports / artifacts)
                │
                ▼
         observation_plane
   (inventory / file tree / telemetry)

OPTIONAL EXTENSION PLANES
- sandbox_plane
- simulation_plane
- cluster_plane
- federation_plane
- service_plane
- publication_plane

REPOSITORY RELATIONSHIP

StegVerse-org/
├── StegVerse-SDK
├── trust-kernel
├── demo_ingest_engine
├── demo_suite_runner
└── StegVerse-demo-suite

StegGhost/
├── entity-sandbox-runner
│   ├── internal_brain/
│   ├── install/
│   ├── incoming_bundles/
│   ├── failed_bundles/
│   ├── installed_bundles/
│   ├── receipts/
│   ├── logs/
│   ├── payload/
│   └── brain_reports/
├── stegverse_sandbox
└── ghost-pat-lab

CURRENT OPERATIONAL INTERPRETATION

entity-sandbox-runner
├── internal_brain/
│   ├── explorer
│   ├── reconciler
│   ├── closure_engine
│   └── actuator
│
├── install/
│   ├── ingestion_v2.py
│   └── engine/
│       ├── receipt_reconciler.py
│       ├── bundle_inventory_engine.py
│       ├── gcat_bcat_evaluator.py
│       ├── next_action_engine.py
│       └── execute_next_action.py
│
├── state surfaces
│   ├── receipts/
│   ├── logs/
│   ├── payload/feedback/
│   └── brain_reports/
│
└── bundle lifecycle
    ├── incoming_bundles/
    ├── installed_bundles/
    └── failed_bundles/

SHORT ARCHITECTURAL READING

- trust-kernel remains the root trust boundary.
- admissibility_plane is where GCAT and BCAT should formally decide whether a transition is allowed.
- receipt_reconciliation_plane is the canonical state surface every engine should eventually depend on.
- decision_plane selects the next admissible action from reconciled state.
- execution_plane performs repair, ingest, retry, rollback, and bundle movement.
- evidence_plane records receipts, reports, and mutation artifacts.
- observation_plane gives human and system visibility into current state.

IMMEDIATE DESIGN NOTE

The current convergence path is:
1. receipts become canonical state input
2. next_action becomes family-aware and trajectory-aware
3. execution writes durable artifacts
4. ingestion confirms movement through incoming -> installed/failed
5. GCAT / BCAT move from descriptive layer into actual admissibility enforcement

# SYSTEM_STATE_v1

## PURPOSE

Stabilize and operate a **closed-loop governed sandbox system** capable of:

- autonomous ingestion
- deterministic decision-making
- controlled execution
- reconciliation and state tracking

This system must:
- operate without external chat context
- derive all decisions from repo state
- converge toward a fully functional repo

---

## CORE LOOP (AUTHORITATIVE)

Single active loop:

ingestion → next_action → execution → reconciliation → ingestion

No parallel systems.
No shadow workflows.
No external decision surfaces.

---

## ACTIVE COMPONENTS

### 1. ORCHESTRATOR
File:
install/autonomous_loop_orchestrator.py

Responsibilities:
- runs the loop
- sequences all stages
- collects outputs
- ensures loop continuity

Status: ✅ WORKING

---

### 2. EXPLORER (OBSERVER)

File:
internal_brain/explorer.py

Responsibilities:
- scans repo state
- identifies:
  - failed bundles
  - installed bundles
  - ingestion reports
  - feedback
  - receipts
- writes:
brain_reports/explore.json

Role:
→ **Observer AI Entity**

Status: ✅ WORKING

---

### 3. NEXT ACTION ENGINE (DECISION)

File:
install/engine/next_action_engine.py

Responsibilities:
- consumes:
  - bundle inventory
  - failed bundle correlations
  - execution history
  - internal brain outputs
- classifies:
  - manifest repairable
  - missing reports
  - unresolved failures
  - obsolete candidates
- selects:
brain_reports/next_action.json

Role:
→ **Proposer AI Entity**

Status: ✅ WORKING (import path fixed)

---

### 4. EXECUTION ENGINE

File:
install/engine/execute_next_action.py

Responsibilities:
- executes selected action
- produces execution result
- enforces sandbox constraints

Role:
→ **Executor AI Entity**

Status: ✅ WORKING

---

### 5. RECONCILIATION ENGINE

File:
install/engine/reconcile_execution_state.py

Responsibilities:
- updates system state after execution
- tracks:
  - success / failure
  - bundle transitions
  - system consistency

Status: ✅ WORKING

---

## SUPPORTING SYSTEMS

### INTERNAL BRAIN

Path:
internal_brain/

Produces:
internal_brain/brain_report.json

Status: ⚠️ PARTIALLY REDUNDANT

---

### BUNDLE SYSTEM

Directories:
failed_bundles/
installed_bundles/
ingestion_reports/

Tracked via:
brain_reports/bundle_inventory.json
brain_reports/failed_bundle_report_correlation.json

Status: ✅ WORKING

---

### STATE SNAPSHOTS

Files:
payload/runtime/system_snapshot_pre.json
payload/runtime/system_snapshot_post.json

Status: ✅ WORKING

---

## CURRENT SYSTEM BEHAVIOR

- loop executes successfully
- explorer detects repo signals
- internal brain produces actions
- next_action_engine selects actions
- execution runs (may idle)
- reconciliation updates state

---

## KNOWN ISSUES

1. Duplicate decision surfaces (internal_brain vs next_action_engine)
2. Partial execution coverage
3. Large unwired module surface

---

## ARCHITECTURAL PRINCIPLE

> Stabilize BEFORE scaling

---

## AI ENTITY MODEL

- Observer → explorer.py
- Proposer → next_action_engine.py
- Executor → execute_next_action.py

---

## CURRENT PRIORITY

Make loop fully operational and self-correcting.

---

## SUCCESS CONDITION

- continuous execution
- no idle failures
- automatic repair of bundles
- deterministic transitions

---

## FINAL NOTE

This is the single source of truth.

END OF SYSTEM STATE

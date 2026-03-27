# SYSTEM_STATE_v2

## PURPOSE

Stabilize and evolve `entity-sandbox-runner` as the **portable self-aware repo sandbox** and **reference governed sandbox pattern** for StegVerse.

This sandbox is not the general customer sandbox itself. It is the internal governed experimental chamber used to determine how three AI entities can be constrained and governed under the GCAT / BCAT formalism while constructing, repairing, and rebuilding the broader repo ecosystem in a way that is legible, replayable, and portable.

---

## ROLE OF ENTITY-SANDBOX-RUNNER

`entity-sandbox-runner` is the **meta-sandbox**.

It exists to:

- inspect failed or questionable artifact histories
- determine likely causes of failure
- propose constrained repairs
- execute bounded repair / rebuild actions
- preserve full local history and replayability
- emit structured artifacts back into bundle lanes for ingestion
- serve as the canonical reference implementation for future portable governed sandboxes

---

## CORE LOOP (AUTHORITATIVE)

Single active loop:

ingestion → snapshot → explore → next_action → execute → reconcile → snapshot

No parallel authoritative loop.
No shadow mutation system.
No direct chat-dependent governance.

---

## CURRENT AI ENTITY MODEL

Three governed AI roles are active conceptually inside the sandbox:

### 1. Observer
Primary surfaces:
- `internal_brain/explore.py`
- `install/engine/repo_snapshot.py`

Responsibilities:
- observe repo state
- observe recent activity
- identify failed bundles
- identify installed bundles
- detect feedback and receipts
- surface candidate pressure

### 2. Proposer
Primary surface:
- `install/engine/next_action_engine.py`

Responsibilities:
- classify failed bundle families
- choose admissible next action
- escalate from inspection to repair proposal when failure persists
- remain deterministic and bounded

### 3. Executor
Primary surfaces:
- `install/engine/execute_next_action.py`
- `install/engine/repair_bundle_engine.py`

Responsibilities:
- execute bounded sandbox actions
- inspect bundle contents
- apply deterministic path-safety repair actions
- never mutate beyond the defined actuator scope

---

## CURRENT WORKING COMPONENTS

### Orchestrator
File:
`install/autonomous_loop_orchestrator.py`

Status:
- working
- reads system state from repo-held markdown
- runs bounded loop
- emits stable runtime report

### Explorer / Observer Surface
File:
`internal_brain/explore.py`

Output:
`brain_reports/explore.json`

Status:
- working
- detects recent failed bundles, installed bundles, ingestion reports, feedback, receipts

### Repo Snapshot
File:
`install/engine/repo_snapshot.py`

Status:
- working
- captures repo state before and after loop execution

### Next Action Engine
File:
`install/engine/next_action_engine.py`

Status:
- working
- supports repair escalation
- can transition from inspection failure to repair proposal

### Execute Engine
File:
`install/engine/execute_next_action.py`

Status:
- working
- performs bounded execution actions

### Repair Bundle Engine
File:
`install/engine/repair_bundle_engine.py`

Status:
- working as minimal v1 actuator
- removes disallowed paths from offending bundles
- rebuilds sanitized bundles
- writes repair reports

### Reconcile Engine
File:
`install/engine/reconcile_execution_state.py`

Status:
- working
- interprets execution result
- classifies failure / ingestion / pending states

---

## CURRENT OBSERVED BEHAVIOR

Confirmed live behaviors:

- sandbox loop runs successfully
- explorer detects repo activity
- internal brain influences next action selection
- next action engine can escalate from inspection to repair proposal
- repair bundle engine can act on path-admissibility failures
- reconcile can reflect whether failure condition persists

This means the sandbox is no longer only observing.
It is now:
- observing
- classifying
- escalating
- acting

---

## KNOWN CURRENT LIMITS

### 1. Repair v1 is path-admissibility only
Current repair engine only enforces path admissibility.

It can:
- remove disallowed files from a bundle
- rebuild compliant structure

It does not yet:
- repair semantic code logic
- repair dependency graphs
- rewrite imports
- rewrite tests
- rewrite manifests beyond minimal structural handling

### 2. Duplicate intelligence surfaces still exist
There are still overlapping observer / proposal influences between:
- `internal_brain`
- `next_action_engine`

This is acceptable temporarily while stabilizing, but long-term only one authoritative proposer surface should remain.

### 3. Reconciliation is still sandbox-local
The sandbox determines local result state, but is not yet integrated into the full CGE-controlled upstream routing cycle.

---

## ARCHITECTURE CORRECTION (AUTHORITATIVE)

The only input into `entity-sandbox-runner` is:

`incoming_bundles/` via ingestion

No direct SDK input.
No direct ADMIN input.
No direct CGE input except through ingestion lane placement.

This sandbox is a governed consumer of ingested artifacts.

---

## CGE / INGESTION ARCHITECTURE

### Correct upstream model

All external or upstream routing is handled through ingestion engines and CGE.

The sandbox does not communicate directly with CGE.

### Authoritative rule

Only ingestion engines communicate **to** CGE and receive artifacts **from** CGE.

Sandboxes communicate only by emitting artifacts into bundle lanes.

---

## CGE OUTPUT LANES

Current CGE output lanes are:

1. `stegverse-org/demo-ingest-engine/`
2. `entity-sandbox-runner/incoming_bundles/`

This means CGE is upstream lane selector and state registrar, while the sandbox is a downstream governed processing unit.

---

## SANDBOX OUTPUT RULE

Sandbox output should only be emitted into local bundle lanes such as:

- `incoming_bundles/`
- `sandbox_bundles/`

Then local ingestion / repo ingestion handles transport toward CGE.

The sandbox should not directly route to CGE.

---

## ENTITY-SANDBOX-RUNNER IN THE BROADER SYSTEM

The broader customer-facing architecture is:

Customer Manifest  
→ SDK  
→ customer ingestion repo  
→ ingestion engine  
→ CGE  
→ proper repo / customer-specific sandbox  
→ experiment execution  
→ receipts / output  
→ ingestion engine  
→ CGE  
→ return lane toward SDK

When faulty iterations occur:

fault history / bundled receipts  
→ CGE  
→ entity-sandbox-runner / incoming_bundles  
→ observer / proposer / executor governed loop  
→ repaired artifacts / receipts / analysis output  
→ sandbox bundle lane  
→ ingestion engine  
→ CGE  
→ record / reroute / retry / archive

That is the intended role of `entity-sandbox-runner`.

---

## PORTABLE SANDBOX CONCEPT

Two portable sandbox classes are emerging.

### 1. Customer experiment sandbox
Purpose:
- run customer-defined experiments
- satisfy customer manifest constraints
- emit structured outputs and chained receipts

### 2. Self-aware repo sandbox
Purpose:
- observe a repo as a whole
- detect broken, duplicated, partial, or obsolete structures
- propose constrained repair / rebuild actions
- execute bounded fixes
- preserve history and replayability
- train the system how to safely reconstruct the ecosystem

`entity-sandbox-runner` is the reference implementation of class (2).

---

## REQUIRED PORTABLE SANDBOX UNIT SHAPE

A portable self-aware repo sandbox should minimally contain:

- ingestion boundary
- observer
- proposer
- executor
- reconciler
- state history engine
- receipt chain
- local bundle lanes

That makes governed self-reconstruction portable.

---

## INGESTION ENGINE PER SANDBOX

A lightweight ingestion boundary per sandbox instance is appropriate.

The sandbox should not be a free-floating computation chamber.
It should be a **portable governed unit** with:

- local ingress
- local egress
- local history
- local bundle lanes

This allows clean sandbox spawning, teardown, replay, and scaling.

---

## STATE HISTORY ENGINE REQUIREMENT

Each portable sandbox should carry local stepwise history, including:

- sandbox_id
- iteration_id
- ingress fingerprint
- input bundle id
- observer findings
- chosen action
- execution result
- reconciliation result
- emitted bundle id
- end-state fingerprint
- timestamps for all steps

This local history is distinct from CGE’s global canonical ledger.

### Separation of roles

- sandbox history = fine-grained local trajectory memory
- CGE history = authoritative global state ledger

---

## CURRENT REPAIR ESCALATION MODEL

Observed live transition:

inspect_failed_bundle_family  
→ reconcile remains failed  
→ next_action escalates to `propose_repair_for_bundle_family`  
→ repair bundle engine can apply deterministic structural repair

This is the first working self-repair transition in the sandbox.

---

## WHAT THE SANDBOX NOW PROVES

The sandbox now demonstrates that a governed three-entity pattern can:

- observe repo failures
- classify pressure and select work
- escalate intelligently when failure persists
- apply bounded structural repairs
- preserve deterministic runtime reports
- move toward portable self-reconstruction

---

## NEXT PRIORITIES

### Immediate
1. Keep loop stable
2. Keep repair escalation deterministic
3. Ensure repaired bundles re-enter ingestion cleanly
4. Preserve reports, receipts, and local state history

### Near-term
1. Add richer repair strategy types beyond path filtering
2. Tighten single authoritative proposer surface
3. Improve reconciliation semantics for repaired bundle reattempts
4. Formalize sandbox-to-ingestion bundle handoff

### Later
1. Clone this portable self-aware repo sandbox into fresh lanes
2. Use it as the reference template for future repair / rebuild cells
3. Derive customer-governed sandboxes from the same structural grammar

---

## SUCCESS CONDITION

This repo reaches success when `entity-sandbox-runner` becomes:

- portable
- self-aware
- replayable
- bounded
- structurally legible
- capable of governed repair / rebuild loops
- suitable as the canonical internal rebuild sandbox for the wider StegVerse ecosystem

---

## FINAL AUTHORITATIVE RULES

1. Repo state, not chat context, is authoritative
2. Only ingestion lanes feed the sandbox
3. Only ingestion engines interface with CGE
4. Sandboxes emit to bundle lanes, not directly to CGE
5. Observer / proposer / executor roles remain distinct
6. Prefer wiring over adding new parallel systems
7. Stabilize first, scale second
8. This sandbox is the reference internal rebuild chamber

END OF SYSTEM STATE

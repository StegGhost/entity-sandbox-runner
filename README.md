# StegVerse Governed Execution + CGE (Canonical Governance Engine)

This repository implements a **deterministic governed execution system** with a **Canonical Governance Engine (CGE)** and an **LLM-agnostic proposal adapter layer**.

---

## 🧠 System Overview

The system enforces **execution-time governance**.

Every action:
- is proposed  
- evaluated  
- admitted or rejected  
- executed only if valid  
- recorded with receipts  
- chained into canonical state  

---

## 🧩 Architecture

```
LLMs / Agents / Planners
        ↓
proposal_adapter.py
        ↓
llm_gateway.py
        ↓
decision_engine.py
        ↓
governed_executor.py
        ↓
buildout engine (phases)
        ↓
receipt chain
        ↓
Merkle tree
        ↓
CGE (Canonical Governance Engine)
        ↓
canonical state + global root
```

---

## 🔐 Core Capabilities

### 1. Governed Execution
- No direct execution from LLMs  
- All actions pass through decision logic  
- Authority resolved at execution time  

---

### 2. Receipt Chain (Deterministic History)
Each phase produces a receipt:
- includes inputs, outputs, validation  
- linked via `parent_hash`  
- tamper-evident  

---

### 3. Merkle Proof Layer
- Merkle tree per run  
- deterministic root  
- verifiable integrity  

---

### 4. Replay Engine
- verifies deterministic execution  
- detects divergence  

---

### 5. Idempotent Build System
- identical inputs → no re-execution  
- returns `"replayed"`  

---

### 6. CGE — Canonical Governance Engine

The CGE is the **state authority layer**.

It:
- stores canonical objects by hash  
- links state across runs  
- produces a global root  
- enables full reconstruction  

---

### 7. State Rebuild

```python
rebuild_state(target_dir, global_root)
```

- reconstructs system state  
- validates integrity  

---

## 🤖 LLM Adapter Layer

LLMs are **proposal sources, not authorities**.

Flow:

```
LLM → proposal_adapter → llm_gateway → decision_engine
```

---

## 📦 Proposal Contract

```json
{
  "model_id": "gpt-5.x",
  "agent_id": "agent_ops",
  "session_id": "session-123",
  "proposal_name": "update_customer_record",
  "authority_id": "local_admin",
  "tool_target": "records.update",
  "payload": {},
  "justification": "...",
  "confidence": 0.86,
  "state_claims": {}
}
```

---

## 🧠 Principle

> This system does not ask: “What happened?”
>  
> It enforces: “What is allowed to happen.”

---

## 🚀 Status

- Deterministic execution ✅  
- Replay + idempotency ✅  
- Receipt chain + Merkle ✅  
- CGE canonical state ✅  
- State rebuild + rollback (v5.1) ✅  

---

## 🔜 Next

- Constraint engine (governance layer)  
- Authority enforcement  
- Policy-driven execution  

---

## ⚡ Category

This is not a workflow tool.

It is:

**A deterministic, verifiable, governed execution system with canonical state.**

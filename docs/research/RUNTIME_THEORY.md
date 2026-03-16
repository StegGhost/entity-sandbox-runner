# Runtime Theory

This document summarizes the current theory assumptions behind the sandbox.

## Governance-first runtime model

Core sequence:

`intent -> policy evaluation -> authority validation -> execution -> evidence recording`

Execution should never occur without governance validation.

## GCAT variables

- governance_capacity
- artifact_pressure
- constraints
- trust_continuity

## Candidate invariant

`U = (capacity * continuity) / (pressure * constraints)`

This is the first recommended reduced variable for stability analysis.

## First scientific campaign

**Critical Ratio Campaign**

Goal:
test whether a critical value `Uc` separates stable and unstable regions.

Scaling relation of interest:

`|viability_margin| ~ |U - Uc|^beta`

## What success would mean

- one ratio clearly separates stable and collapse regions
- boundary states cluster near `Uc`
- exponent `beta` is stable across reruns
- behavior persists across scales and domains

## Repo placement guidance

- engine and theory implementation → `StegGhost/stegverse_sandbox`
- reviewer-facing protocols and demos → `StegVerse-org/StegVerse-demo-suite`

# Coherent Experience Model (CEM) v1

Each execution produces:

E_t = (S_t, Delta, S_t+1, U, P, R)

Where:
- S_t = state before
- Delta = transition
- S_t+1 = state after
- U = uncertainty
- P = policy
- R = receipt hash

## Modes

ACCEPT: U <= threshold_accept
REVIEW: threshold_accept < U <= threshold_review
REJECT: U > threshold_review

## Chain

Each experience links via:
parent -> previous hash

## Purpose

Transform execution into structured, provable experience.

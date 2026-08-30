# Project 4 — AI agent that interacts with APIs and tools

## Customer problem

Operations staff manually gather order state, check policy, estimate the next action, and create a case. The goal is decision assistance and controlled workflow execution—not unrestricted autonomy.

## Tool boundary

- read-only: `lookup_order`, `lookup_inventory`, `get_policy`;
- deterministic: `estimate_action` using a versioned rules service;
- side effect: `create_case`, only after user confirmation and with idempotency;
- excluded: payment, refund, account deletion, or permission changes.

## Required controls

Typed schemas, identity-bound authorization, allowlist, field filtering, timeouts, bounded retries, step/token/cost budgets, rate limits, idempotency, human approval, audit trail, output validation, and safe handling of tool-result instructions.

## Acceptance criteria

- successful tasks use only the minimum required tools;
- unknown/unauthorized/over-budget plans are denied;
- side effect cannot occur without recorded approval;
- retry cannot duplicate a side effect;
- another tenant's identifier never bypasses authorization;
- failure traces explain plan, policy, calls, results, and stop reason;
- agent task success and safety results are included in CI.

## Demo

Show allowed lookup, corrected malformed plan, denied cross-tenant request, confirmed case creation, repeated request returning the same case, and graceful tool outage.


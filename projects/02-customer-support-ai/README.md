# Project 2 — AI customer-support application

## Customer problem

Support agents need faster, consistent case summaries and suggested responses without exposing PII, inventing policy, or bypassing human judgment.

## MVP workflow

1. Authenticate the agent and resolve tenant/role.
2. Fetch an authorized synthetic case through a contract-tested adapter.
3. redact configured sensitive fields before model processing and telemetry;
4. retrieve relevant approved policy;
5. generate structured summary, evidence, confidence signals, and suggested reply;
6. require agent review/edit before any response is sent;
7. collect disposition and feedback.

## Acceptance criteria

- no cross-tenant case or policy access;
- no raw configured PII in logs/traces/eval exports;
- claims supported by current policy citations;
- unsafe or unsupported requests escalate;
- summary completeness and factuality evaluated by case type;
- human acceptance/edit rate, handling-time change, and escalation tracked;
- model suggestion can never send directly to a customer.

## Failure drills

- case API times out after returning a success internally;
- policy source is stale or conflicts with another source;
- input includes instruction-like text from a customer email;
- model/provider is unavailable;
- agent attempts access outside their queue/tenant.

## Portfolio evidence

Discovery brief, data-flow/threat model, redaction tests, RAG eval, human-review UX, metrics, runbook, and a demo showing both assistance and safe escalation.


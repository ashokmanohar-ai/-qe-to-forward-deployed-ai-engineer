# Lab 8 — Lead a production AI incident

## Scenario

At 09:10 UTC, p95 latency rises from 2.1 s to 8.7 s. Model cost per successful task triples. HTTP error rate stays low, but customer feedback reports stale and incomplete answers. Only one region and two high-volume tenants are affected.

At 08:55, three changes occurred:

- retrieval `top_k` changed from 5 to 20;
- a model provider routing rule changed;
- one vector-store replica began reporting memory pressure.

Correlation is not causation. Test each hypothesis.

## Exercise timeline

1. **0-10 minutes:** assess impact, severity, owners, mitigation options, and update cadence.
2. **10-25 minutes:** compare healthy/affected segments and stage-level traces.
3. **25-40 minutes:** apply the safest reversible mitigation and verify user symptoms.
4. **40-60 minutes:** construct the evidence timeline and communicate recovery.
5. **Afterward:** perform root-cause and contributing-factor analysis.

## Questions

- Why can HTTP success remain high while task success falls?
- Which signal distinguishes provider latency from retrieval context growth?
- Could retry behavior amplify cost and saturation?
- What evidence proves rollback restored both quality and latency?
- What guardrail should have caught this before broad rollout?

## Deliverables

- incident roles and timestamped action log;
- two customer updates;
- impact and affected-segment analysis;
- mitigation and recovery verification;
- root cause, contributing factors, and non-causes;
- corrective actions with owners, priority, and due dates;
- updated alert, canary gate, and runbook.

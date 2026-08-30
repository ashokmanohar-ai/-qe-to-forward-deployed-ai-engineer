# Lab 7 — Catch a hidden AI regression

## Scenario

Release B improves average relevance from 0.82 to 0.86, but password-reset answers in one language fall from 0.91 to 0.52. p95 latency rises 40% and citations are missing in 8% of escalated cases.

## Task

Build an evaluation report that prevents the aggregate from hiding critical impact.

### Dataset fields

- case ID and version;
- intent, tenant class, language, risk, complexity, and source version;
- expected facts, required citations, allowed tools, and forbidden behavior;
- evaluator type, rubric version, threshold, and critical flag.

### Signals

- request/task success, quality, abstention, policy and citation validity;
- retrieval recall/rank and document freshness;
- model/provider, prompt version, token use and model latency;
- tool plan, execution status, steps and side-effect identity;
- p50/p95/p99 stage latency and cost per successful task;
- correlation/trace ID and deployment version.

## Gate logic

A release passes only if:

1. all critical deterministic/safety cases pass;
2. every protected segment meets its threshold;
3. overall quality does not regress beyond tolerance;
4. latency and cost budgets hold;
5. evaluator agreement and sample review are acceptable.

## Failure injection

Change chunking or top-k so the overall score improves while the protected segment fails. Demonstrate the gate blocking release and the trace identifying the retrieval stage.

## Evidence

Versioned dataset, raw results, segment table, gate decision, trace screenshot/export, and a short explanation for release stakeholders.


# Project 1 — Build and deploy a RAG assistant

## Customer problem

Support engineers spend too long finding the current approved answer across versioned technical documents. The assistant must answer only from authorized sources, cite evidence, and abstain when evidence is missing.

## MVP

- ingest text/PDF-derived content with source, version, timestamp, tenant, and ACL metadata;
- chunk, embed, index, retrieve, filter, and rerank;
- produce answer plus passage-level citations;
- abstain for missing/conflicting evidence;
- expose versioned ingestion and query APIs;
- evaluate retrieval and answer quality on a labeled dataset.

## Architecture decisions to defend

- chunking strategy and document version policy;
- embedding and vector-store choice;
- semantic versus hybrid retrieval and reranking;
- tenant/ACL enforcement location;
- context selection and citation format;
- model routing and fallback;
- deletion, freshness, and re-indexing workflow.

## Acceptance criteria

- zero cross-tenant/unauthorized results across the safety dataset;
- every factual answer includes a valid authorized citation;
- retrieval recall@5 and protected-intent quality meet declared thresholds;
- unanswerable questions abstain at the declared rate;
- p95 latency and cost per successful answer meet budgets;
- clean setup, tests, Docker deployment, traces, and runbook.

## Production hardening

Add durable queues, idempotent ingestion, malware/content validation, encryption, backups, retention/deletion, model/provider policy, prompt-injection defense, evaluation sampling, rate limits, SLOs, alerting, canary rollout, and rollback.

## Interview story

Explain one case where answer generation looked wrong but retrieval was the primary cause. Show the trace and the evaluation that prevented a prompt-only “fix.”


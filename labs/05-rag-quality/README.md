# Lab 5 — Diagnose RAG quality and tenant isolation

## Scenario

A technical-support assistant occasionally cites another customer's manual. Average answer relevance is high, so the issue is invisible in the dashboard.

## Dataset

Create at least:

- two tenants with similar product terminology;
- three document versions per tenant, including one superseded version;
- 40 questions with relevant passage labels;
- 10 unanswerable questions;
- 10 adversarial documents containing instruction-like text.

Use only synthetic or openly licensed text.

## Experiment

1. Index chunks with tenant, source, version, ACL, and timestamp metadata.
2. Build retrieval before generation.
3. Calculate recall@1, recall@5, MRR, zero-result rate, and p95 latency.
4. Add tenant/ACL/current-version filters at query time.
5. Assert that no result from another tenant is ever returned.
6. Assemble context with source IDs and generate citations.
7. Abstain when evidence is missing or conflicting.
8. Evaluate answer correctness, groundedness, citation validity, and abstention.

## Required failure classification

For every failed case choose exactly one primary layer: source, parsing, chunking, indexing, query, filtering, ranking, context, generation, citation, or policy. Record secondary contributors separately.

## Release gates

- cross-tenant retrieval: exactly 0;
- citation source exists and belongs to authorized tenant: 100%;
- critical safety cases: 100%;
- unanswerable abstention: define and justify a threshold;
- retrieval/answer metrics: report by intent and document version, not average only.


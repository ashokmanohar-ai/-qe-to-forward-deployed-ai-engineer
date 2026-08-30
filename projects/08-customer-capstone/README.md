# Project 8 — Forward Deployed AI customer capstone

## Objective

Solve one realistic customer problem from discovery through handover. This is the portfolio centerpiece.

## Recommended problem

A multi-tenant enterprise wants an assistant that answers from approved documents and can create a support case after explicit user confirmation. It must integrate with existing identity and case APIs, protect tenant data, meet a p95 latency target, and launch a limited pilot in four weeks.

You may substitute a domain you know, but preserve real identity, data, integration, evaluation, deployment, and operational constraints.

## Phase 1 — Discover

- stakeholder/user/system map;
- current workflow and quantified baseline;
- problem statement and non-AI alternative;
- measurable success and non-goals;
- data, security, integration, operational, timeline, and budget constraints;
- assumption log and riskiest unknowns.

## Phase 2 — Design

- context/container/sequence/failure diagrams;
- identity, authorization, tenant, and data-lifecycle boundaries;
- API/tool schemas and source-of-truth map;
- model, retrieval, evaluation, observability, and deployment decisions;
- threat model, ADRs, risk register, and rollout plan.

## Phase 3 — Build the vertical slice

- authenticated API;
- versioned synthetic document ingestion;
- tenant-filtered retrieval, citations, and abstention;
- bounded `create_case` tool with confirmation/idempotency;
- tests and segment-aware evaluation;
- Docker, Kubernetes, CI, Terraform example, metrics, traces, and audit.

## Phase 4 — Validate

Test functionality, contracts, AI quality, prompt injection, tenant isolation, tool safety, performance, capacity, reliability, cost, usability, and recovery. Record raw evidence and limitations.

## Phase 5 — Deploy and operate

Run a canary/pilot plan, alert drill, dependency outage, rollback, secret rotation simulation, and production incident exercise. Hand the runbook to another engineer and observe whether it is usable.

## Phase 6 — Communicate

Deliver:

- 5-minute executive demo: outcome, evidence, risk, next decision;
- 30-minute technical review: architecture, trade-offs, validation, operations;
- public case study: sanitized context, your contribution, results, failure learned, next step;
- interview defense: alternate architecture, scale, security, cost, and incident questions.

## Completion gates

- no critical security/tenant/tool-safety failure;
- declared quality thresholds pass by protected segment;
- latency, reliability, and cost budgets are evidenced;
- clean checkout is reproducible;
- deployment and rollback are demonstrated;
- production gaps are explicit, owned, and not disguised as complete;
- customer value is connected to a measured baseline.

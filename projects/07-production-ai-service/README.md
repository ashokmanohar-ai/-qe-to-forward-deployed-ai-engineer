# Project 7 — Production-ready AI service

## Goal

Build a versioned service with authentication, authorization, persistence, AI orchestration, evaluation, monitoring, testing, and CI/CD.

## Minimum architecture

- API gateway/service with identity and tenant authorization;
- relational system of record and durable work queue;
- document/vector retrieval with ACL filters;
- model-provider interface with timeout, rate limit, fallback, and budget;
- policy/evaluation layer;
- structured logs, metrics, distributed traces, and audit events;
- container/Kubernetes/Terraform deployment;
- pipeline gates and rollback.

## Non-functional acceptance

- threat model covers input, retrieval, model, tool, data, telemetry, and pipeline boundaries;
- SLOs include task success and quality, not only availability;
- load test reports tail latency, saturation, errors, quality, and cost;
- backup/restore, data deletion, secret rotation, model/prompt change, and incident runbooks exist;
- dependency outage degrades safely;
- every release is traceable to code, configuration, prompts, models, indexes, and eval results.

Use `src/qe_fde/ai_service` as a learning reference, not as an assertion that an in-memory demo is production-ready.


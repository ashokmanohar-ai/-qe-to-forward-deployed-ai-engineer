# Project 6 — LLM observability dashboard

## Goal

Create an operational view that connects user impact to application, retrieval, model, tool, infrastructure, quality, and cost signals.

## Required views

- task success, availability, p50/p95/p99 latency, and error by deployment;
- stage-level latency for routing, retrieval, model, tool, and policy;
- retrieval recall proxy, zero-result rate, source freshness, and tenant-filter failures;
- model/provider/prompt version, tokens, throttle/fallback, and cost per successful task;
- agent steps, tool failures, approval, duplicate prevention, and stop reasons;
- online quality/feedback by protected segment;
- release annotations and incident links.

## Trace requirements

Use a single correlation path, safe attribute allowlist, redaction, sampling policy, retention, and role-based access. Link dashboards to representative traces without storing secrets or raw sensitive content.

## Acceptance criteria

Given a latency/quality/cost regression, the dashboard narrows the failing stage and affected segment within ten minutes and links to evidence needed for mitigation.

## Failure drill

Increase retrieval top-k and enable an unnecessary retry. Show how context size increases model latency/cost and how the dashboard distinguishes this from provider degradation.


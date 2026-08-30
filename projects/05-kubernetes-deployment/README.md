# Project 5 — Deploy an AI application with Docker and Kubernetes

## Goal

Turn a working AI service into an operable workload with immutable artifacts, external configuration, least privilege, health semantics, scaling, rollout, rollback, and evidence.

## Deliverables

- minimal non-root image and software bill of materials;
- Deployment, Service, ConfigMap, Secret reference, NetworkPolicy, HPA, and disruption strategy;
- startup/readiness/liveness probes with documented semantics;
- resource requests/limits based on measurements;
- CI build, test, scan, sign/provenance (where available), and deploy stages;
- canary or rolling release with automatic/manual rollback criteria;
- SLOs, dashboards, alerts, and operations runbook;
- local cluster path and one cloud deployment design.

## Failure drills

Bad secret, wrong port binding, failing dependency, OOM kill, CPU throttling, provider rate limit, node loss, partial rollout, and network-policy denial.

## Acceptance criteria

A reviewer can deploy from a clean checkout, observe version/health, scale, introduce a known failure, diagnose it, and roll back without rebuilding the artifact.


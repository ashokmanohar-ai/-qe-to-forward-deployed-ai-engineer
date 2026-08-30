# 24-Week Progress Roadmap

Use this file for a visible checklist or use `fde-roadmap` for a local interactive tracker. A checked box means the evidence exists and another engineer can inspect it—not merely that the material was read.

## Before Week 1

- [ ] Complete the [QE-to-FDE baseline assessment](docs/skill-bridge.md#baseline-assessment).
- [ ] Install Python, Git, Docker, and a code editor.
- [ ] Fork or clone this repository and run `make validate`.
- [ ] Create a private learning journal for customer-sensitive notes.
- [ ] Choose one domain for the capstone: education, healthcare, finance, retail, logistics, or another domain you understand.

## Stage 1 — Foundation

### Week 1: Python for builders

- [ ] Complete Lab 1 and repair the API client.
- [ ] Add type hints, structured exceptions, logs, and unit tests.
- [ ] Explain retry safety and non-retryable errors in the pull request.
- [ ] Record evidence: commit, tests, and design note.

### Week 2: Git, Linux, networking, and runtime basics

- [ ] Resolve a merge conflict without discarding another person's work.
- [ ] Trace a request through DNS, TCP/TLS, HTTP, process, and application layers.
- [ ] Use process, port, disk, memory, and log tools to test hypotheses.
- [ ] Record evidence: debugging journal and root-cause explanation.

### Week 3: SQL, data modeling, and data quality

- [ ] Model customer, document, event, evaluation, and feedback data.
- [ ] Write joins, aggregates, window functions, and an explain-plan review.
- [ ] Add uniqueness, foreign-key, null, range, and freshness gates.
- [ ] Record evidence: schema, queries, tests, and profiling report.

### Week 4: REST APIs and backend services

- [ ] Build a versioned FastAPI service with typed request/response models.
- [ ] Add API-key authentication, idempotency, timeouts, and structured errors.
- [ ] Test success, validation, authorization, retry, and failure behavior.
- [ ] Record evidence: OpenAPI contract, tests, and ADR.

### Week 5: Software and system design

- [ ] Separate domain logic from framework and external-system code.
- [ ] Draw context, container, request-sequence, and failure-path diagrams.
- [ ] Explain sync/async, cache, queue, database, consistency, and availability trade-offs.
- [ ] Pass the Stage 1 exit review.

## Stage 2 — Cloud and Deployment

### Week 6: Docker and container security

- [ ] Create a reproducible multi-stage or minimal container build.
- [ ] Run as non-root with dropped capabilities and external configuration.
- [ ] Add startup, readiness, and liveness behavior that reflects real dependencies.
- [ ] Record image size and vulnerability results.

### Week 7: Kubernetes fundamentals

- [ ] Deploy with Deployment, Service, ConfigMap, Secret reference, and resource limits.
- [ ] Scale and roll out a new version, then perform a rollback.
- [ ] Diagnose an image, configuration, probe, scheduling, and network failure.
- [ ] Publish a Kubernetes operations runbook.

### Week 8: CI/CD and GitHub Actions

- [ ] Run lint, type, unit, integration, documentation, and security checks.
- [ ] Use least-privilege workflow permissions and protected deployment environments.
- [ ] Produce immutable artifacts and preserve test/evaluation evidence.
- [ ] Demonstrate that a failing gate prevents release.

### Week 9: AWS, Azure, and GCP

- [ ] Map compute, containers, identity, secrets, object storage, SQL, NoSQL, networking, observability, and AI services.
- [ ] Select one primary cloud based on customer constraints.
- [ ] Explain portability boundaries without claiming feature equivalence.
- [ ] Record a weighted cloud decision matrix.

### Week 10: Terraform and production deployment

- [ ] Format, validate, plan, and apply the local Terraform example.
- [ ] Explain state, locking, drift, modules, providers, and secret handling.
- [ ] Define metrics, logs, traces, alerts, ownership, rollback, and cleanup.
- [ ] Pass the Stage 2 exit review.

## Stage 3 — AI Engineering

### Week 11: LLM fundamentals

- [ ] Explain tokens, context, sampling, latency, cost, hallucination, and model limits.
- [ ] Compare models with a fixed dataset and repeatable settings.
- [ ] Separate model, prompt, retrieval, tool, and application behavior.
- [ ] Publish an experiment report with limitations.

### Week 12: Structured prompting

- [ ] Define task, context, constraints, examples, output schema, and abstention behavior.
- [ ] Test ambiguous, malformed, adversarial, multilingual, and long inputs.
- [ ] Version prompts and connect changes to evaluation results.
- [ ] Demonstrate schema validation and safe error handling.

### Week 13: Embeddings and vector databases

- [ ] Build a representative retrieval dataset with relevance labels.
- [ ] Compare chunk size, overlap, embedding, top-k, filter, and reranking choices.
- [ ] Measure recall@k, MRR, latency, and tenant-filter correctness.
- [ ] Publish retrieval results and trade-offs.

### Week 14: RAG

- [ ] Build ingestion, retrieval, context assembly, generation, citations, and abstention.
- [ ] Trace each stage and attribute failures correctly.
- [ ] Test stale, conflicting, missing, malicious, and wrong-tenant documents.
- [ ] Release Portfolio Project 1.

### Week 15: Agents and tools

- [ ] Define typed tools with minimal permissions and bounded inputs/outputs.
- [ ] Add timeouts, retries, idempotency, approvals, budgets, and audit events.
- [ ] Test invalid plans, unavailable tools, partial failure, loops, and unsafe requests.
- [ ] Produce a readable agent trace and side-effect policy.

### Week 16: Evaluation and AI quality

- [ ] Create versioned golden, adversarial, safety, and production-derived datasets.
- [ ] Combine deterministic, retrieval, model-graded, human, and online evaluation.
- [ ] Segment results by risk, intent, tenant, language, and complexity.
- [ ] Release Portfolio Project 3 and pass the Stage 3 exit review.

## Stage 4 — Forward Deployed Engineering

### Week 17: Customer discovery

- [ ] Identify users, decisions, workflows, pain, baseline, value, constraints, and risks.
- [ ] Separate problem, requested feature, proposed solution, assumption, and fact.
- [ ] Define measurable success, non-goals, rollout guardrails, and open questions.
- [ ] Deliver a two-page discovery brief.

### Week 18: Solution architecture and integration

- [ ] Map systems, owners, data classification, identity, interfaces, and operational boundaries.
- [ ] Design the smallest end-to-end vertical slice.
- [ ] Create contracts, sequence/failure diagrams, threat model, ADRs, and risk register.
- [ ] Lead a design review and incorporate evidence-based feedback.

### Week 19: Rapid prototype and production plan

- [ ] Time-box the riskiest unknowns and build a usable vertical slice.
- [ ] Demonstrate normal, failure, and recovery paths using representative data.
- [ ] Separate prototype shortcuts from production commitments.
- [ ] Deliver a phased plan with owners, dependencies, risks, and acceptance gates.

### Week 20: Production incident and communication

- [ ] Establish severity, impact, timeline, ownership, and the next update time.
- [ ] Mitigate before pursuing a perfect root cause.
- [ ] Preserve evidence and distinguish correlation from causation.
- [ ] Publish a blameless incident review and pass the Stage 4 exit review.

## Stage 5 — Advanced Production AI

### Week 21: Security, identity, and secrets

- [ ] Threat-model user, retrieval, model, tool, API, pipeline, and operator boundaries.
- [ ] Test prompt injection, data leakage, excessive agency, abuse, and supply-chain risk.
- [ ] Design authentication, authorization, tenant isolation, secret rotation, and audit.
- [ ] Record residual risks and explicit customer decisions.

### Week 22: Reliability, observability, and performance

- [ ] Define user-facing SLIs/SLOs for availability, latency, task success, quality, and freshness.
- [ ] Correlate traces across gateway, orchestration, retrieval, model, and tools.
- [ ] Test alerts, retry budgets, fallback, degradation, and recovery runbooks.
- [ ] Demonstrate one investigation using telemetry rather than intuition.

### Week 23: Scalability and cost

- [ ] Model normal, peak, burst, and adversarial workloads.
- [ ] Measure p50/p95/p99 latency, throughput, saturation, errors, quality, and cost per successful task.
- [ ] Test batching, caching, model routing, asynchronous work, and backpressure.
- [ ] Explain every optimization's quality and reliability trade-off.

### Week 24: Capstone and interview loop

- [ ] Release the customer capstone with reproducible setup and evidence.
- [ ] Run a failure drill and hand the runbook to another engineer.
- [ ] Present a 5-minute executive story and 30-minute technical review.
- [ ] Complete the six-part mock interview and close priority gaps.
- [ ] Publish a concise case study and final reflection.

## Completion definition

- [ ] At least three deep portfolio projects are public and reproducible.
- [ ] Each project has tests, evals, architecture, security assumptions, deployment, telemetry, and a runbook.
- [ ] The capstone demonstrates discovery through production operations.
- [ ] Mock interview scores are at least 3/4 in every competency, with no critical security or customer-judgment miss.
- [ ] Your resume and GitHub profile describe outcomes and evidence rather than tool lists.

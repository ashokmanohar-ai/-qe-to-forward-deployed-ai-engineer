# Stage 5 — Advanced Production AI

**Weeks 21-24 · Exit outcome:** defend the capstone's security, reliability, scalability, evaluation, cost, and rollout decisions in an interview loop.

## Week 21: Threat-model the complete path

Map trust boundaries from user to gateway, orchestrator, retrieval, model, tools, data stores, telemetry, pipeline, and operator.

### Threat categories

| Boundary | Example threats | Example controls |
|---|---|---|
| User/input | abuse, prompt injection, oversized input | authentication, limits, policy, content handling |
| Retrieval | indirect injection, poisoned/stale source, tenant leak | provenance, ACL filters, sanitization, versioning, evals |
| Model/provider | leakage, retention, unsafe output, supply change | data policy, contractual controls, routing, output validation |
| Tools | excessive agency, confused deputy, duplicate side effect | least privilege, user-bound auth, allowlists, approval, idempotency |
| API/data | broken auth, insecure direct object access, exfiltration | centralized authorization, tenant keys, encryption, audit |
| Pipeline | malicious dependency/action, secret theft, artifact tamper | pinning, scanning, OIDC, protected environments, provenance |
| Observability | PII or secrets in traces and prompts | classification, redaction, access, sampling, retention |

For every risk, record asset, threat actor, path, impact, likelihood, prevention, detection, response, owner, and residual decision.

### Injection principle

Retrieved content and tool output are data, not authority. They cannot grant permissions or redefine the system's trusted instructions.

## Week 22: Reliability and observability

Define user-facing SLIs:

- availability of the complete task, not only HTTP 200;
- p50/p95/p99 end-to-end latency and per-stage latency;
- task success and critical-segment quality;
- retrieval freshness and source coverage;
- safe abstention/escalation correctness;
- tool success without duplicate side effects;
- cost per successful task.

### Trace shape

```text
request
├── authenticate + authorize
├── classify / route
├── retrieve
│   ├── embed query
│   ├── vector search + filters
│   └── rerank
├── model inference
├── tool call (optional)
├── output policy + citations
└── evaluation sampling
```

Propagate one correlation identifier, but never place secrets or raw sensitive data in it or in span attributes.

## Week 23: Optimize the system, not only the model

Create a workload model with request mix, document sizes, retrieval top-k, prompt/output tokens, tool frequency, concurrency, peak/burst pattern, provider quotas, and growth.

Measure:

- throughput and p50/p95/p99 latency;
- error, timeout, retry, throttle, and fallback rates;
- CPU, memory, connections, queue depth, and saturation;
- retrieval and quality metrics by segment;
- input/output tokens and cost per attempted and successful task.

Test optimization candidates one at a time:

- cache safe, versioned, non-personal results;
- batch embeddings or asynchronous work;
- reduce irrelevant context rather than blindly truncating;
- route simple tasks to smaller models with evaluation gates;
- add backpressure and bounded queues;
- precompute reusable retrieval features;
- use circuit breakers and graceful degradation.

Reject an optimization if it improves averages while violating a critical quality, security, or tail-latency target.

## Week 24: Capstone defense

Your final package contains:

- discovery brief and baseline;
- measurable success and non-goals;
- architecture, contracts, ADRs, and threat model;
- working vertical slice with representative synthetic data;
- versioned test and evaluation datasets;
- quality, safety, performance, reliability, and cost results;
- Docker/Kubernetes/Terraform and CI/CD;
- telemetry, SLOs, alerts, runbooks, rollback, and incident review;
- production gap analysis and phased rollout;
- five-minute executive demo and 30-minute technical review.

### Three-audience exercise

Explain the same design to:

1. **Executive:** outcome, risk, investment, evidence, next decision.
2. **Architect:** boundaries, trade-offs, security, scale, integration, operations.
3. **On-call engineer:** signals, dependencies, failure modes, mitigation, recovery.

## Stage review

Use the [interview scoring rubric](../interview/roadmap.md). A critical miss in authorization, tenant isolation, unsafe tool execution, data handling, or customer integrity blocks completion even if the aggregate score is high.

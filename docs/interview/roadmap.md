# Forward Deployed Engineer (AI) interview roadmap

## Typical interview loop

| Area | What is assessed | Evidence to practice |
|---|---|---|
| Practical coding | Python clarity, correctness, tests, trade-offs | API/data/queue exercises |
| Debugging | hypotheses, evidence, prioritization, recovery | logs, traces, broken service |
| AI/LLM | system understanding, evaluation, safety | RAG/agent failure analysis |
| System design | requirements, architecture, scale, security, operations | customer AI service design |
| Customer case | discovery, ambiguity, judgment, communication | scenario role-play |
| Experience | ownership, conflict, incidents, outcomes, learning | structured project stories |

## Six-week preparation plan

### Week 1 — Python and data

- implement LRU cache, rate limiter, retry policy, bounded queue, and streaming parser;
- parse nested JSON into typed models and validate error paths;
- write SQL for latest-version selection, deduplication, rolling metrics, and tenant isolation;
- practice explaining time/space complexity and production trade-offs.

### Week 2 — APIs and debugging

- design and implement an idempotent endpoint;
- integrate a rate-limited paginated API with checkpoints;
- diagnose timeout, TLS, DNS, connection-pool, and retry-storm evidence;
- write a 15-minute incident update and a root-cause outline.

### Week 3 — LLM, RAG, agents, and evaluation

- explain model/context/token/sampling behavior without marketing terms;
- design retrieval evaluation before tuning generation;
- compare RAG, fine-tuning, tool use, and deterministic software;
- threat-model prompt injection and excessive agency;
- design offline, human, and online evaluation with segmentation.

### Week 4 — Cloud and system design

- design a secure multi-tenant AI assistant for 10, 1,000, and 100,000 concurrent users;
- reason about queues, caching, state, rate limits, backpressure, regions, and consistency;
- describe container, Kubernetes, CI/CD, Terraform, identity, secrets, observability, and rollback;
- calculate a simple latency and cost budget.

### Week 5 — Customer cases and communication

- run all four customer scenarios;
- ask discovery questions for 15 minutes before proposing architecture;
- give executive, architect, and operator versions of the same answer;
- practice saying “AI is not the first problem to solve” with evidence and an alternative.

### Week 6 — Full mocks and gap closure

- run two complete interview loops under time constraints;
- score with the rubric below;
- fix the two weakest evidence gaps;
- rehearse capstone demo, failure drill, and lessons learned;
- prepare questions that reveal role scope, customer ownership, deployment responsibility, and success criteria.

## Practical coding exercises

### 1. Bounded API adapter — 45 minutes

Implement a typed client for a paginated API with timeouts, retryable status classification, exponential backoff injection, checkpointing, and tests. Discuss rate limits, duplicate pages, partial output, and observability.

### 2. Tenant-aware document retrieval — 60 minutes

Given in-memory documents, implement ranking plus mandatory tenant/ACL/version filters. Return citations and abstain below a threshold. Add tests proving cross-tenant results are impossible.

### 3. Idempotent tool execution — 60 minutes

Implement a side-effecting `create_case` boundary that accepts an idempotency key and request hash. Handle repeated same request, conflicting reuse, ambiguous timeout, and concurrent calls.

### 4. Evaluation aggregation — 45 minutes

Given case-level JSON results, calculate overall and segment metrics and block release when any critical case or protected segment fails. Avoid division/empty-segment errors and explain statistical limitations.

### 5. Debug a slow service — 30 minutes

Receive request, retrieval, model, and tool spans. Determine the primary bottleneck, distinguish retries from legitimate calls, propose mitigation, and identify missing telemetry.

## Python question bank

- When use dataclass, Pydantic model, TypedDict, protocol, or abstract base class?
- How do generators help process large data without unbounded memory?
- What do async I/O and concurrency solve, and what do they not solve?
- How would you make retry logic testable without sleeping?
- How do exception boundaries affect API contracts and observability?
- What makes a function safe to retry?
- How do you prevent race conditions around an idempotency record?
- How would you profile CPU, memory, I/O, and event-loop blocking?

## APIs, SQL, and data question bank

- Design errors and versioning for a customer integration API.
- Explain authentication versus authorization with a tenant example.
- How do you safely paginate a changing dataset?
- When use a queue instead of a synchronous API call?
- How do transactions, isolation, unique constraints, and upserts support idempotency?
- How do schema migrations remain backward compatible?
- How do you track source and derived-data lineage for RAG?
- How do you delete a customer document and its embeddings safely?

## AI/LLM question bank

- Why can temperature zero still fail to give identical results?
- When choose prompting, RAG, fine-tuning, tools, or deterministic logic?
- How do you evaluate retrieval separately from generation?
- What causes a grounded answer with an invalid citation?
- How do chunking, filters, top-k, reranking, and context limits interact?
- What can an LLM-as-judge measure, and how do you calibrate it?
- How do you prevent an aggregate metric from hiding a critical regression?
- Why is retrieved content untrusted, and how do you handle indirect injection?
- What controls make a tool-calling workflow safe?
- How do you detect model, data, prompt, retrieval, and behavior drift?

## Cloud and production question bank

- Design identity and secrets for GitHub Actions deploying to cloud without long-lived keys.
- What is the difference between startup, readiness, and liveness?
- How do requests/limits, autoscaling, queues, and provider quotas interact?
- What should be in logs, metrics, traces, and audit—and what must not be?
- How do you set an SLO for an AI task rather than an endpoint?
- How do you roll out a prompt/model/index change safely?
- What happens when a tool times out after completing a side effect?
- How would you reduce cost without silently reducing quality?

## System-design exercises

### Multi-tenant enterprise assistant

Design ingestion and querying for millions of versioned documents across 500 tenants. Include SSO, ACLs, regional data constraints, citations, deletion, evals, rate limits, cost, observability, and incident recovery.

### Customer-support copilot

Design a human-reviewed drafting assistant connected to case and policy systems. Include PII, prompt injection from customer text, policy freshness, evaluation, feedback, and phased rollout.

### API operations agent

Design a workflow that reads system state and can create a ticket after confirmation. Include tool schemas, identity propagation, idempotency, partial failure, audit, budgets, and restricted actions.

### Evaluation platform

Design a service that runs datasets across models/prompts/retrievers, supports deterministic/model/human evaluators, stores traceable results, segments risk, and gates CI at enterprise scale.

For each exercise, clarify users, scale, baseline, success, data, constraints, non-goals, and rollout before drawing components.

## Customer-facing scenarios

Practice answers to:

- The customer insists on a model/framework you believe is unsuitable.
- The executive wants production in two weeks, but identity and data access are unresolved.
- A pilot demo is strong, but evaluation coverage is weak.
- Security blocks a tool permission required by the proposed workflow.
- The model performs poorly in one high-risk segment but well overall.
- Customer and product teams disagree about success.
- A production incident may have exposed another tenant's citation.

Strong answers surface impact and evidence, protect trust, propose reversible paths, assign decisions to the right owners, and communicate uncertainty honestly.

## Experience story bank

Prepare six stories using **Context → Stakes → Your decision → Actions → Evidence → Outcome → Learning**:

1. ambiguous requirement turned into a measurable outcome;
2. difficult production/root-cause investigation;
3. quality or security risk you escalated constructively;
4. system/framework you designed and drove to adoption;
5. disagreement resolved through evidence and trade-offs;
6. failure or wrong assumption that changed your approach.

Do not describe only team activity. State your responsibility, decision, evidence, and measurable outcome.

## Scoring rubric

Score 0-4 for each:

| Competency | 0 | 2 | 4 |
|---|---|---|---|
| Problem framing | jumps to tools | asks basic requirements | finds root outcome, baseline, constraints, non-goals |
| Coding | unsafe/incomplete | working happy path | clear contract, tests, failures, trade-offs |
| AI reasoning | model folklore | basic RAG/agent concepts | layered evaluation, failure attribution, safety |
| Architecture | component list | workable design | trust/failure/operations/scale/cost decisions |
| Debugging | random fixes | tests one hypothesis | prioritizes impact, evidence, mitigation, verification |
| Security | ignored | lists controls | applies identity/data/agency boundaries and residual risk |
| Customer communication | jargon or overpromises | understandable | audience-specific, honest, decisive, value-linked |
| Ownership | waits for direction | completes assigned work | drives ambiguity to evidence, decision, delivery, handover |

Readiness target: at least 3 in every area. Any critical security, data-integrity, or deceptive customer-communication miss is a fail regardless of average.

## Questions to ask the interviewer

- What percentage of time is discovery, prototyping, production engineering, and incident support?
- Who owns deployed customer systems after launch?
- What access does the FDE have to customer environments and data?
- How are security, evaluation, and production-readiness decisions made?
- What distinguishes a successful first 90 days?
- How are reusable product capabilities separated from customer-specific work?
- What is the escalation model when customer urgency conflicts with safety or reliability?


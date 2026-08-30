# QE-to-FDE skill bridge

## Transfer map

| QE capability | Keep using it for | FDE extension | Portfolio proof |
|---|---|---|---|
| Test design | Model user goals, branches, constraints, and risk | Convert workflows into eval datasets and rollout gates | Traceable scenario/eval matrix |
| Automation frameworks | Compose reusable workflows and integrations | Own production Python modules, APIs, and tool contracts | Typed service with tests |
| API testing | Validate contracts, auth, errors, and reliability | Design and operate versioned integrations | OpenAPI spec + idempotency tests |
| UI/product analysis | Understand real behavior and user friction | Run customer discovery and prototype workflow changes | Discovery brief + demo |
| CI/CD | Automate repeatable quality gates | Build secure artifact and deployment pipelines | Least-privilege Actions workflow |
| Debugging and RCA | Form hypotheses and isolate causes | Diagnose distributed, data, model, retrieval, and tool paths | Trace-led incident review |
| Performance testing | Design workload and find bottlenecks | Model AI latency, token cost, provider limits, and queueing | Load/cost report |
| Security testing | Think adversarially and validate boundaries | Threat-model prompt injection, data leakage, agency, and supply chain | AI threat model + abuse tests |
| Reporting | Explain evidence and risk | Communicate decisions, status, and trade-offs to customers | Executive brief + technical appendix |

## The main gaps to close

### 1. From test code to product code

You need to own domain models, packages, interfaces, persistence, concurrency, migrations, backward compatibility, error semantics, and maintainability—not only test clients and fixtures.

### 2. From pipeline user to deployment owner

You need to reason about images, runtime identity, networks, secrets, health, resource limits, rollouts, rollback, telemetry, capacity, and cloud cost.

### 3. From deterministic assertions to AI evaluation

You need versioned datasets, retrieval labels, rubric design, model graders, human review, segmentation, confidence, drift, and online signals. An average score is not a release strategy.

### 4. From requirements recipient to discovery partner

You need to ask why, expose assumptions, establish a baseline, identify decision makers and system owners, quantify value, define non-goals, and say when AI is the wrong solution.

### 5. From defect report to operating decision

You need to make reversible decisions under uncertainty, mitigate incidents, communicate impact and next steps, and drive ownership across customer and engineering teams.

## Baseline assessment

Score each competency from 0 to 4:

- **0 — Unknown:** cannot explain the concept.
- **1 — Aware:** can describe it but not perform it.
- **2 — Assisted:** can complete a guided task.
- **3 — Independent:** can deliver and troubleshoot it alone.
- **4 — Teaches/owns:** can make trade-offs, review others, and operate it in production.

| Competency | Target before Stage 1 | Target after Week 24 | Your score |
|---|---:|---:|---:|
| Python application development | 1 | 3 | |
| Git, Linux, networking | 2 | 3 | |
| REST APIs and backend design | 2 | 3 | |
| SQL and data pipelines | 1 | 3 | |
| System design | 1 | 3 | |
| Docker and Kubernetes | 1 | 3 | |
| CI/CD and IaC | 2 | 3 | |
| Cloud architecture | 1 | 3 | |
| LLM and prompting concepts | 1 | 3 | |
| Embeddings, vector search, and RAG | 0 | 3 | |
| Agents and tool safety | 0 | 3 | |
| AI evaluation and observability | 1 | 4 | |
| Security and reliability | 2 | 3 | |
| Customer discovery | 1 | 3 | |
| Executive and technical communication | 2 | 3 | |
| Incident leadership | 2 | 3 | |

### Interpret your scores

- Do not spend equal time everywhere. Invest first in any target competency below 2.
- QE candidates often start stronger in testing, CI, debugging, and risk. Use that advantage to move faster through familiar concepts while producing stronger AI evaluation evidence.
- Re-score at Weeks 5, 10, 16, 20, and 24. A score increases only when you can point to evidence.

## Role-readiness signal

You are approaching FDE readiness when you can handle this prompt end to end:

> A customer wants an AI assistant connected to internal documents and ticketing tools. Data is multi-tenant, some actions change customer records, latency must stay under three seconds for most requests, and the customer wants a pilot in four weeks.

Without jumping straight to a framework, you should be able to:

1. run discovery and challenge the request;
2. define success, non-goals, risk, and rollout boundaries;
3. design the identity, data, retrieval, model, tool, evaluation, and observability architecture;
4. build a vertical slice;
5. test quality, security, performance, and failure;
6. deploy and operate it;
7. explain what is ready, what is not, and what should happen next.


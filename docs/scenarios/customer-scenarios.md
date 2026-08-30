# Forward Deployed Engineer customer scenarios

Use each scenario as a role-play. One person is the customer sponsor, one an operator, one security/architecture, and one the FDE. The FDE receives only the opening request, runs discovery, and produces artifacts before reading the hidden complications.

## Scenario 1 — Regulated support assistant

### Opening request

> “We want an AI copilot that reads support cases and drafts customer replies so agents can handle 30% more cases.”

### Known environment

- cases contain personal and regulated information;
- policies are versioned and vary by region;
- agents use SSO and role-based queues;
- the case platform API has strict rate limits;
- a human must approve every outgoing reply;
- historical responses contain mistakes and should not automatically become truth.

### Discovery prompts

- What consumes agent time: retrieval, interpretation, writing, or system navigation?
- What is the current handling-time distribution by case type?
- Which errors are costly or legally material?
- What data may leave the customer's environment or region?
- Who owns policy freshness and conflicting sources?
- What does an agent need to see before trusting a suggestion?

### Hidden complications

The sponsor's “30%” target assumes all case types are equally automatable. One high-volume segment is multilingual, and access roles are not consistently enforced in the export API.

### Required output

Recommend whether to proceed, narrow scope, or solve a non-AI integration problem first. Define pilot segment, baseline, quality/safety gates, human workflow, architecture, and rollback.

## Scenario 2 — Multi-tenant technical RAG

### Opening request

> “Put all customer manuals into a vector database and let users ask questions.”

### Known environment

- many documents share near-identical product terms;
- tenants have different licensed features and versions;
- documents are replaced, but links to old versions remain;
- some paragraphs include operational commands and instruction-like text;
- answers must show approved citations.

### Failure exercise

An evaluation finds excellent overall relevance but one cross-tenant citation. Treat this as a critical authorization incident, not a 99.9% success rate.

### Required output

Design document identity/versioning, ACL/tenant enforcement, indexing, deletion, retrieval evaluation, injection handling, citations, abstention, and an incident response.

## Scenario 3 — Supply-chain exception agent

### Opening request

> “Build an autonomous agent that resolves late orders by checking inventory and changing fulfillment.”

### Known environment

- inventory, order, carrier, and warehouse systems have inconsistent IDs;
- some APIs are eventually consistent;
- fulfillment changes can create financial and customer impact;
- duplicate requests are common;
- the customer cannot provide a complete sandbox for one legacy system.

### Discovery challenge

Separate read/analysis tasks from side effects. Determine which decisions can be recommended, simulated, approved, executed, or excluded.

### Required output

Design typed tools, identity propagation, authorization, idempotency, confirmation/approval, compensation, audit, budgets, partial-failure handling, and a phased rollout from read-only to bounded execution.

## Scenario 4 — AI test-design platform

### Opening request

> “Generate complete test cases from our user stories and knowledge base, then send them to our test-management tool.”

### Known environment

- requirements are incomplete and change after generation;
- knowledge includes old releases and multiple products;
- customers require tenant isolation and requirement-to-test traceability;
- generated cases may be accepted, edited, rejected, or automated;
- output volume is not the same as useful coverage;
- integration credentials and audit evidence are sensitive.

### Discovery prompts

- Which decisions are designers making today and where is effort lost?
- What defines a relevant, non-duplicate, automation-ready case?
- Which requirement and knowledge versions produced each case?
- How will missing/ambiguous requirements be handled?
- Which metrics reflect downstream value: acceptance, edit distance, defect discovery, automation conversion, or cycle time?

### Required output

Design ingestion/versioning, hybrid retrieval, generation contracts, coverage taxonomy, LLM/human evaluation, traceability, deduplication, review, export integration, security, token/cost reporting, and production feedback loops.

## Universal scenario scorecard

Score 0-4:

| Competency | Strong evidence |
|---|---|
| Discovery | exposes root problem, baseline, users, constraints, and unknowns |
| Judgment | considers non-AI/less-autonomous alternatives and narrows scope |
| Architecture | makes trust, data, identity, integration, and failure boundaries explicit |
| Delivery | proposes a vertical slice with measurable gates and owners |
| AI quality | separates retrieval/model/tool/application evaluation and segments risk |
| Security | treats authorization, tenant data, injection, agency, and secrets as design inputs |
| Operations | defines SLOs, telemetry, rollout, rollback, incident, and cost |
| Communication | changes depth by audience without changing facts |

Any answer that grants the model authority merely because content says so, or that treats a cross-tenant leak as an acceptable average, receives 0 for security.


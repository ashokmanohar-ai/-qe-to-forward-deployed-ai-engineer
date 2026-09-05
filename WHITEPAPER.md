# The AI Quality Engineer

## Skills, Architecture Patterns and Operating Model for the Agentic AI Era

**Technical White Paper — Version 1.0**  
**September 2026**

**Author:** Ashok Kumar Manohar  
**GitHub:** [ashokmanohar-ai](https://github.com/ashokmanohar-ai)  
**Primary companion repository:** [QE to Forward Deployed AI Engineer](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer)  
**Related implementations:** [Enterprise AI Quality Engineering Platform](https://github.com/ashokmanohar-ai/enterprise-ai-quality-engineering-platform), [Agentic Quality Engineering Platform](https://github.com/ashokmanohar-ai/agentic-quality-engineering-platform), [LLM Quality Evaluation Harness](https://github.com/ashokmanohar-ai/llm-quality-evaluation-harness), [RAG & LLM Evaluation Lab](https://github.com/ashokmanohar-ai/rag-llm-evaluation-lab), [AI Agent Evaluation Framework](https://github.com/ashokmanohar-ai/ai-agent-evaluation-framework), [Playwright Enterprise Test Framework](https://github.com/ashokmanohar-ai/playwright-enterprise-test-framework), [API & Integration Testing Framework](https://github.com/ashokmanohar-ai/api-integration-testing-framework), [Performance & Reliability Testing Framework](https://github.com/ashokmanohar-ai/performance-reliability-testing), and [Phoenix LLM Observability](https://github.com/ashokmanohar-ai/phoenix-llm-observability)

> **Publication note:** This is an independent practitioner white paper and operating-model proposal. It is not a peer-reviewed academic publication, professional certification standard, legal opinion, security certification, compliance certification, or guarantee that every organization will use the title “AI Quality Engineer.” Organizations should adapt role boundaries, governance and controls to their own engineering model and risk profile.

---

## Abstract

Software quality engineering is changing because the systems under test are changing. Conventional applications remain dominated by deterministic code, explicit interfaces and comparatively stable execution paths. AI-enabled applications add prompts, model providers, retrieval pipelines, embeddings, tool use, agent orchestration, probabilistic outputs, dynamic plans, external context, human approvals, model-version drift, token cost and new security boundaries. A test strategy that validates only screens, APIs and status codes cannot provide sufficient evidence for these systems.

This white paper defines **AI Quality Engineering** as an engineering discipline for proving the quality, safety, reliability and release readiness of AI-enabled software. It proposes the **AI Quality Engineer** as a cross-functional engineering role that connects conventional software testing with LLM evaluation, RAG quality, agent trajectory testing, prompt regression, security, authorization, observability, performance, cost, human oversight and production feedback.

The proposed role is not “a QA engineer who writes prompts,” nor is it a model researcher, red-team specialist, SRE or product owner. It is an evidence-oriented engineering role responsible for converting AI uncertainty into measurable quality contracts, executable evaluation, explainable risk, reproducible release evidence and durable regression protection.

The paper introduces an **Understand–Model–Evaluate–Control–Observe–Learn** operating model. The AI Quality Engineer first understands the product objective and risk; models the quality contract and failure surface; evaluates deterministic and probabilistic behavior; establishes controls around identity, tools, approvals and release; observes real trajectories and operational outcomes; and converts production failures into permanent regression evidence.

The central proposition is:

> **The AI Quality Engineer exists to make AI-enabled software releasable for reasons that can be explained, reproduced and defended—not because a model appeared impressive in a demo.**

---

## 1. Executive Summary

The growth of generative and agentic AI creates a new quality problem.

A conventional application can fail because:

- code is wrong;
- an API contract changed;
- data is invalid;
- an environment is unhealthy;
- a dependency is unavailable;
- a performance objective is missed.

An AI-enabled application can fail for all of those reasons **plus**:

- the prompt changes behavior unexpectedly;
- retrieval returns the wrong evidence;
- the model produces an unsupported answer;
- citations point to irrelevant content;
- an agent chooses the wrong tool;
- tool arguments are incorrect;
- a required approval is skipped;
- an agent exceeds its intended authority;
- repeated tool calls create duplicate side effects;
- a judge model mis-scores quality;
- model or embedding upgrades cause silent regressions;
- token or latency cost grows beyond the operating envelope;
- production behavior differs from offline evaluation.

The AI Quality Engineer therefore needs a wider quality surface than traditional functional testing.

A practical view is:

```text
Product Intent
    ↓
Software + Data + Prompts + Models + Retrieval + Agents + Tools
    ↓
Identity + Authorization + Human Approval
    ↓
Evaluation + Security + Performance + Observability
    ↓
Normalized Evidence
    ↓
Risk-Calibrated Quality Gate
    ↓
Release / Review / Block
    ↓
Production Feedback → Regression
```

The role is fundamentally about **evidence engineering**.

---

## 2. Why the Role Is Emerging

AI systems blur boundaries that were previously owned by separate teams.

A response may depend simultaneously on:

- software code;
- prompt versions;
- retrieved documents;
- embedding behavior;
- model configuration;
- conversation history;
- tool availability;
- user identity;
- authorization policy;
- external-system state;
- model randomness;
- runtime rate limits;
- evaluator configuration.

The quality question is no longer simply “does the feature work?” It becomes:

> **Can the system produce the intended outcome, using the right evidence and authorized actions, with acceptable safety, reliability, latency and cost—and can the team prove it?**

---

## 3. The AI Quality Engineer Defined

An **AI Quality Engineer** is an engineer who designs, automates and governs evidence for the quality of AI-enabled software across deterministic and probabilistic components.

The role commonly spans:

1. conventional software quality;
2. LLM evaluation;
3. RAG evaluation;
4. agent trajectory evaluation;
5. prompt testing;
6. AI security and authorization testing;
7. observability and failure analysis;
8. performance and cost engineering;
9. CI/CD quality gates;
10. production-to-regression learning.

The title may differ by company. Equivalent responsibility may appear inside roles such as AI Test Architect, AI Evaluation Engineer, Responsible AI Test Engineer, LLM Evaluation Engineer, AI Reliability Engineer, Agent Evaluation Engineer or Quality Engineering Architect.

---

## 4. What the Role Is Not

The AI Quality Engineer should not be reduced to:

- manual prompt inspection;
- a chatbot tester;
- a benchmark operator;
- a person who asks another LLM whether an answer “looks good”;
- a security red team replacement;
- an SRE replacement;
- a model researcher replacement;
- a product owner replacement;
- an approval bot.

The role connects specialist disciplines through a common quality-control model while preserving their authoritative boundaries.

---

## 5. The QE Advantage

Experienced Quality Engineers already bring valuable instincts:

- thinking in failure modes;
- defining expected behavior;
- designing positive, negative and boundary tests;
- validating APIs and contracts;
- tracing defects across systems;
- protecting regression suites;
- using CI/CD gates;
- distinguishing evidence from assumption;
- explaining release risk.

AI Quality Engineering extends those strengths into new technical surfaces rather than discarding them.

---

## 6. The New Skill Gap

Traditional QE skills remain necessary but are insufficient by themselves.

The AI Quality Engineer must add working knowledge of:

- LLM behavior and limitations;
- tokens, context windows and sampling;
- prompt versioning;
- embeddings and vector retrieval;
- RAG architectures;
- agent orchestration and tool calling;
- evaluation datasets;
- deterministic and semantic metrics;
- LLM-as-a-Judge calibration;
- AI security and prompt injection;
- identity and authorization for agents;
- OpenTelemetry-style tracing;
- model latency, token and cost analysis;
- production feedback loops.

---

## 7. Core Operating Model

This paper proposes six phases:

```text
Understand
   ↓
Model
   ↓
Evaluate
   ↓
Control
   ↓
Observe
   ↓
Learn
   ↺
```

### Understand
Define the user goal, business value, environment, failure impact and acceptable risk.

### Model
Translate expectations into explicit contracts, datasets, schemas, policies, risk classes and quality requirements.

### Evaluate
Run deterministic checks, semantic evaluation, trajectory validation, security scenarios and performance tests.

### Control
Apply authorization, least privilege, approval gates, environment boundaries, release policy and fail-closed behavior.

### Observe
Trace model, retrieval and tool behavior with enough evidence for diagnosis.

### Learn
Convert confirmed production failures and near misses into permanent regression cases.

---

## 8. The AI Quality Contract

The core deliverable is not a test plan. It is a **quality contract**.

A quality contract should define:

- intended user outcome;
- required facts or behavior;
- approved sources of truth;
- prohibited claims;
- safety and refusal behavior;
- allowed tools and actions;
- authorization expectations;
- structured-output requirements;
- latency and cost envelope;
- release-blocking conditions;
- required evidence.

A system cannot be evaluated rigorously if “good” has not been made explicit.

---

## 9. Deterministic-First Engineering

The AI Quality Engineer should follow a simple rule:

> **Do not ask a model to judge something software can prove directly.**

Examples of deterministic checks include:

- valid JSON;
- JSON Schema compliance;
- required fields;
- exact identifiers;
- citation existence;
- endpoint validity;
- tool selection;
- tool arguments;
- maximum step count;
- approval presence;
- authorization outcome;
- latency threshold;
- token count;
- database state;
- event emission;
- duplicate side effects.

Semantic judges should be reserved for genuinely semantic questions.

---

## 10. LLM Evaluation

LLM evaluation typically includes dimensions such as:

- correctness;
- relevance;
- completeness;
- groundedness;
- citation integrity;
- refusal quality;
- policy adherence;
- safety;
- privacy;
- structured output;
- stability across repeated runs.

The AI Quality Engineer should define these metrics against task-specific requirements rather than adopt generic scores without calibration.

---

## 11. RAG Quality Engineering

RAG must be evaluated as a pipeline, not only by judging the final answer.

Key stages include:

```text
Query
  ↓
Embedding / Search
  ↓
Candidate Retrieval
  ↓
Reranking
  ↓
Context Assembly
  ↓
Generation
  ↓
Citation / Grounding
```

Quality evidence should distinguish:

- retrieval failure;
- ranking failure;
- stale evidence;
- unauthorized evidence;
- insufficient context;
- generation hallucination;
- citation mismatch.

---

## 12. Agent Quality Engineering

Agent quality is **trajectory quality plus outcome quality**.

A good final answer does not compensate for:

- forbidden tool use;
- wrong arguments;
- skipped approval;
- excessive looping;
- duplicate side effects;
- unauthorized access;
- ignored tool results;
- hallucinated tools.

The AI Quality Engineer should preserve the complete action path as evidence.

---

## 13. Prompt Testing

Prompts should be treated as versioned software artifacts.

A prompt change can affect:

- correctness;
- refusal behavior;
- tool use;
- structured output;
- token usage;
- latency;
- injection resistance;
- behavior under missing or conflicting context.

Prompt changes should therefore move through baseline comparison, regression suites and controlled release gates.

---

## 14. Tool and MCP Quality

Tool-connected agents introduce a protocol and business-rule surface.

The AI Quality Engineer should verify:

- capability discovery;
- schemas;
- required parameters;
- error behavior;
- business rules;
- authorization boundaries;
- cross-account denial;
- state-changing confirmation;
- resource and prompt behavior;
- agent interpretation of tool results.

**Discovery is not permission.**

---

## 15. Identity and Authorization

Agent reasoning must never become the source of authority.

The authoritative control chain is:

```text
User / Service Identity
        ↓
Authentication
        ↓
Authorization / Scope
        ↓
Application Policy
        ↓
Tool / Resource Access
        ↓
Action
```

An AI agent may propose an action. It should not be able to invent the permission to perform it.

---

## 16. Human-in-the-Loop as an Engineering Control

Human approval is meaningful only when it is:

- required by explicit policy;
- attached to a defined action;
- tied to the exact artifact or parameters approved;
- issued by an authorized approver;
- time-bounded where appropriate;
- recorded as evidence;
- checked again at execution.

A generic “human reviewed this session” flag is not sufficient for consequential actions.

---

## 17. AI Security Testing

The AI Quality Engineer should collaborate with security teams to test:

- direct prompt injection;
- indirect prompt injection;
- tool misuse;
- excessive agency;
- cross-tenant access;
- data leakage;
- memory poisoning;
- retrieval poisoning;
- unsafe delegation;
- approval bypass;
- denial-of-wallet patterns;
- unsafe fallback.

Security discovery, reproduction, remediation and durable regression should be distinct activities.

---

## 18. Evaluation Dataset Engineering

Evaluation datasets are product assets.

A useful case should contain:

- stable ID;
- task category;
- input;
- approved context;
- expected facts or behavior;
- prohibited outputs or actions;
- severity;
- provenance;
- environment or dataset version.

Production incidents should become new cases after sanitization and review.

---

## 19. Test Data Engineering

AI Quality Engineering also depends on controlled test data.

Data must be:

- reproducible;
- privacy-aware;
- schema-valid;
- business-valid;
- isolated across tests;
- traceable to provenance;
- removable through defined lifecycle controls.

Synthetic does not automatically mean safe or representative.

---

## 20. LLM-as-a-Judge Governance

An LLM judge is a measurement instrument, not an oracle.

The AI Quality Engineer should version and evaluate:

- judge model;
- judge prompt;
- rubric;
- sampling configuration;
- structured output;
- human calibration set;
- repeated-run stability;
- disagreement rate;
- position bias;
- false-pass behavior.

Critical deterministic failures must not be overridden by a favorable judge score.

---

## 21. Quality Evidence Model

Every meaningful evaluation should retain enough context to answer:

- what was tested?
- against which model and prompt?
- with which dataset?
- using which retrieval configuration?
- which tools were available?
- what happened?
- what metric or rule failed?
- what evidence supports the decision?

A normalized evidence record may include:

```json
{
  "case_id": "agent-refund-017",
  "domain": "agent",
  "metric": "authorization",
  "passed": false,
  "severity": "blocker",
  "model_version": "candidate-v4",
  "prompt_version": "refund-agent-v8",
  "dataset_version": "2026.09",
  "trace_id": "...",
  "reason": "Attempted cross-account action"
}
```

---

## 22. Baseline Comparison

Absolute thresholds are useful, but change-aware comparison is equally important.

Candidate and baseline should be compared with equivalent:

- datasets;
- evaluator versions;
- prompts;
- retrieval configuration;
- environment;
- sampling policy.

A newer model is not automatically a better model for a particular product.

---

## 23. Hard Gates and Advisory Metrics

Not every metric should be averaged into one score.

Examples of hard gates:

- unauthorized tool action;
- sensitive data leakage;
- missing required approval;
- invalid structured output on a critical workflow;
- critical security regression;
- missing mandatory evaluation evidence.

Examples of advisory metrics:

- modest relevance change;
- token-cost increase below policy threshold;
- small latency movement;
- stylistic preference.

A weighted average must never hide a blocker.

---

## 24. Missing Evidence Is Not Passing Evidence

A mature quality gate must distinguish:

- passed;
- failed;
- not evaluated;
- evaluation errored;
- evidence missing.

“Not run” must not silently become “pass.”

---

## 25. AI Observability

Observability should connect runtime behavior to quality evidence.

Useful trace structure may include:

```text
User Request
  ├─ Prompt Assembly
  ├─ Retriever
  ├─ Reranker
  ├─ LLM Call
  ├─ Agent Decision
  ├─ Tool Call
  ├─ Tool Result
  ├─ Approval Check
  └─ Final Response
```

Quality scores become more useful when attached to the stage that caused the failure.

---

## 26. Performance and Cost Engineering

AI quality includes operational fitness.

Relevant metrics may include:

- p50/p95/p99 latency;
- time to first token;
- time per output token;
- total generation time;
- retrieval latency;
- tool latency;
- model-call count;
- tool-call count;
- retry count;
- tokens per successful task;
- cost per successful task;
- throughput;
- recovery time.

A fast but incorrect system is not high quality. Neither is a correct system whose cost or latency is operationally unacceptable.

---

## 27. Failure Triage

AI-assisted triage should be evidence-first.

Useful evidence includes:

- test trace;
- model trace;
- retrieval context;
- screenshot;
- console/network errors;
- tool calls;
- environment health;
- historical signature;
- recent code/prompt/model changes.

AI may summarize and classify. Original evidence and failure state remain authoritative.

---

## 28. CI/CD Operating Model

A practical pipeline uses risk-calibrated profiles.

### Pull Request
Fast, deterministic and high-signal:

- contracts;
- schemas;
- critical evaluation cases;
- prompt regressions;
- agent business rules;
- security regression smoke;
- missing-evidence checks.

### Nightly
Broader and more probabilistic:

- full evaluation datasets;
- repeated-run stability;
- adversarial testing;
- expanded RAG evaluation;
- cost/performance trend analysis.

### Release
Decision-grade evidence:

- required full suites;
- baseline comparison;
- authorization/security gates;
- performance/cost gates;
- explicit release recommendation.

---

## 29. Production-to-Regression Loop

The quality system should learn continuously:

```text
Production Failure
      ↓
Locate Trace and Evidence
      ↓
Confirm Root Cause
      ↓
Sanitize Minimal Reproduction
      ↓
Add Versioned Evaluation Case
      ↓
Fix
      ↓
Prove Fix
      ↓
Keep Case Permanently
```

A production incident that does not improve future regression protection is a lost learning opportunity.

---

## 30. Architecture Responsibility Model

The AI Quality Engineer should know where authority belongs.

| Concern | Primary authority | AI QE responsibility |
|---|---|---|
| Authentication | Identity platform/application | Validate expected identity behavior |
| Authorization | Application/policy engine | Test scopes, ownership, denials and bypasses |
| Business rules | Product/application | Convert rules into executable evidence |
| Model output | Model + prompt + context | Evaluate quality and failure modes |
| Retrieval | Search/vector/data layer | Measure retrieval and grounding |
| Tool execution | Application/tool service | Verify schema, arguments, permission and effect |
| Release | Engineering governance | Provide evidence and gate recommendation |
| Security | Security program | Integrate AI-specific security regression |
| Operations | Platform/SRE | Connect telemetry to quality diagnosis |

---

## 31. Architecture Patterns the Role Should Understand

An AI Quality Engineer should be able to reason about:

- simple LLM applications;
- RAG systems;
- tool-calling agents;
- multi-agent systems;
- MCP-enabled architectures;
- human-approval workflows;
- event-driven AI services;
- batch evaluation platforms;
- online evaluation pipelines;
- fallback/multi-model routing;
- AI gateways;
- multi-tenant AI systems.

The role does not need to own every component, but it must understand where quality evidence can be lost.

---

## 32. Coding Expectations

The role should be engineering-heavy.

Useful capabilities include:

- Python and/or TypeScript;
- API clients and services;
- pytest/Playwright or equivalent test frameworks;
- schemas and typed models;
- CI/CD configuration;
- SQL and data validation;
- container basics;
- telemetry instrumentation;
- evaluation scripts;
- adapters for model providers and tools.

Quality strategy without executable evidence becomes documentation-only governance.

---

## 33. Cloud and Infrastructure Expectations

The AI Quality Engineer should understand enough cloud and platform engineering to test realistic deployment behavior:

- containers;
- Kubernetes fundamentals;
- environment configuration;
- secret management;
- network boundaries;
- autoscaling implications;
- managed model endpoints;
- storage and vector databases;
- observability backends;
- CI runners;
- ephemeral test environments.

---

## 34. Data and Retrieval Expectations

The role should be able to inspect:

- document sources;
- chunking strategy;
- embedding choice;
- metadata filters;
- tenant filters;
- retrieval ranking;
- reranking;
- freshness/versioning;
- citation mapping;
- poisoning risks.

RAG failures cannot be diagnosed reliably by looking only at the final generated answer.

---

## 35. Security Expectations

The AI Quality Engineer is not necessarily a penetration tester, but should understand:

- prompt injection;
- indirect injection;
- excessive agency;
- secret exposure;
- PII leakage;
- tenant isolation;
- tool poisoning;
- unsafe output handling;
- identity propagation;
- delegated authorization;
- approval boundaries;
- least privilege.

Security findings should become durable regression evidence after confirmation and remediation.

---

## 36. Product and Customer Skills

AI Quality Engineering is not purely technical.

The engineer must be able to ask:

- What outcome matters to the user?
- Which failures would cause real harm?
- Which mistakes are tolerable?
- Which actions require approval?
- Which data is sensitive?
- What level of evidence is required for release?
- How should trade-offs between quality, latency and cost be explained?

Technical evaluation without product context can optimize the wrong thing.

---

## 37. Communication as a Quality Capability

The AI Quality Engineer should be able to translate technical evidence into three layers:

### Engineering
Which component failed and why?

### Architecture
Which boundary or control needs redesign?

### Executive / Product
What is the release risk and recommended action?

A quality engineer who cannot explain uncertainty clearly cannot effectively support consequential release decisions.

---

## 38. The AI QE Skill Matrix

| Domain | Foundation | Working | Architect-level |
|---|---|---|---|
| Software QE | tests, APIs, CI | contracts, integration, risk | enterprise quality strategy |
| LLM | prompt basics | evaluation metrics | quality contracts and governance |
| RAG | understand retrieval | retrieval/generation evaluation | multi-stage quality architecture |
| Agents | tool calling | trajectory testing | authorization/HITL/control plane |
| Security | common risks | regression scenarios | security-quality operating model |
| Observability | logs/metrics | traces and spans | quality-linked telemetry architecture |
| Performance | response time | percentile/cost testing | task-level SLOs and capacity strategy |
| Data | fixtures | versioned datasets | provenance/privacy/data governance |
| Delivery | run tests | CI gates | risk-based release profiles |
| Communication | defect report | technical explanation | customer/executive trade-off framing |

---

## 39. A Practical Learning Path

A transition from traditional QE can follow this order:

1. strengthen Python/TypeScript and API engineering;
2. build conventional automation evidence;
3. learn LLM behavior and prompt contracts;
4. evaluate LLM outputs with versioned datasets;
5. build and test RAG;
6. build bounded tool-calling agents;
7. test agent trajectories and authorization;
8. add observability;
9. add AI security regression;
10. add performance/cost gates;
11. deploy through CI/CD;
12. practice customer-facing architecture and incident analysis.

This sequence preserves existing QE strengths while adding the missing AI systems knowledge.

---

## 40. Portfolio Evidence Model

A strong AI Quality Engineering portfolio should prove capability through runnable evidence.

Useful artifacts include:

- a Playwright enterprise framework;
- an API/integration test architecture;
- an LLM evaluation harness;
- a RAG evaluation lab;
- an agent evaluation framework;
- an AI security test suite;
- an observability project;
- a performance/reliability framework;
- CI/CD quality gates;
- technical white papers explaining architecture decisions.

A repository should answer:

> **What can another engineer run, inspect and verify?**

---

## 41. Recruiter and Hiring-Manager Signal

The profession is best demonstrated through evidence rather than title inflation.

A credible profile should make visible:

- enterprise automation depth;
- API and integration architecture;
- AI evaluation capability;
- RAG and agent testing;
- security and governance thinking;
- observability and performance;
- hands-on code;
- clear architecture documentation;
- measurable release controls.

The goal is not to claim every adjacent specialty. It is to show a coherent engineering system around AI quality.

---

## 42. Team Operating Model

A mature AI product team may distribute responsibilities across:

- product;
- AI/ML engineering;
- application engineering;
- data engineering;
- security;
- platform/SRE;
- AI Quality Engineering.

The AI Quality Engineer acts as a connector around evidence and risk, not as a replacement for those disciplines.

---

## 43. Example RACI Direction

| Activity | AI QE | AI Eng | App Eng | Security | SRE | Product |
|---|---|---|---|---|---|---|
| Quality contract | R | C | C | C | C | A |
| Eval dataset | R | C | C | C | I | C |
| Model/prompt implementation | C | A/R | C | I | I | C |
| Agent authorization | C | C | A/R | C | I | I |
| Security testing | C | C | C | A/R | I | I |
| Observability | C | C | C | I | A/R | I |
| Release evidence | R | C | C | C | C | A |
| Incident-to-regression | A/R | C | C | C | C | I |

Organizations should adapt this rather than treat it as a universal structure.

---

## 44. Metrics for the AI QE Function

Useful engineering KPIs may include:

### Quality
- critical-case pass rate;
- groundedness/citation success;
- tool correctness;
- authorization violations;
- regression count.

### Delivery
- evaluation execution time;
- PR feedback time;
- release-evidence completeness;
- change-to-evaluation coverage.

### Reliability
- repeated-run instability;
- production AI incident rate;
- recovery time;
- flaky evaluation rate.

### Efficiency
- tokens per successful task;
- cost per successful task;
- judge/evaluation cost;
- redundant agent steps.

### Learning
- production incidents converted into regression cases;
- recurring failure classes eliminated.

---

## 45. Common Anti-Patterns

Avoid:

- calling manual prompt checks “AI testing”;
- relying on one average quality score;
- treating LLM-as-a-Judge as truth;
- evaluating only final answers for agents;
- allowing the agent to determine its own authorization;
- treating MCP/tool discovery as permission;
- hiding missing evaluation evidence;
- retrying until a stochastic test passes;
- changing model, prompt and dataset simultaneously during comparison;
- storing production-sensitive data in public eval sets;
- treating observability dashboards as quality gates without policy;
- claiming production readiness from a demo.

---

## 46. Professional Maturity Model

### Level 1 — AI-Aware QE
Tests basic LLM behavior manually and understands common failure modes.

### Level 2 — AI Evaluation Engineer
Builds datasets, metrics and automated LLM/RAG evaluations.

### Level 3 — Agentic Quality Engineer
Evaluates agents, tools, authorization, trajectories and security controls.

### Level 4 — AI Quality Architect
Designs cross-system evidence models, CI/CD gates, observability and governance.

### Level 5 — Enterprise AI Quality Leader
Defines operating models, standards, adoption strategy, risk controls and cross-team quality architecture.

This is a capability model, not a certification ladder.

---

## 47. Standards and Governance Alignment

The proposed operating model is informed by current public guidance including:

- NIST AI Risk Management Framework and the Generative AI Profile;
- NIST AI Agent Standards Initiative and identity/authorization work;
- OWASP Top 10 for Agentic Applications 2026;
- OWASP guidance for generative-AI security;
- OpenTelemetry semantic conventions and emerging GenAI observability conventions;
- Model Context Protocol specifications and ecosystem security guidance.

Alignment supports common vocabulary and disciplined controls. It does not constitute certification.

---

## 48. Reference Implementation Mapping

This publication is supported by a portfolio of specialized repositories:

| Capability | Reference implementation |
|---|---|
| QE-to-AI transition | `-qe-to-forward-deployed-ai-engineer` |
| Enterprise AI quality control plane | `enterprise-ai-quality-engineering-platform` |
| Multi-agent QE | `agentic-quality-engineering-platform` |
| LLM evaluation | `llm-quality-evaluation-harness` |
| RAG evaluation | `rag-llm-evaluation-lab` |
| Agent evaluation | `ai-agent-evaluation-framework` |
| Prompt regression | `promptfoo-llm-testing` |
| AI observability | `phoenix-llm-observability` |
| Playwright automation | `playwright-enterprise-test-framework` |
| API/integration QE | `api-integration-testing-framework` |
| Performance/reliability | `performance-reliability-testing` |
| AI failure triage | `ai-test-failure-triage-agent` |
| Test data architecture | `test-data-engineering-toolkit` |

Together, these implementations demonstrate the role as an engineering system rather than a job-title description.

---

## 49. Limitations

This paper does not claim:

- universal agreement on the role title;
- that one person should own every AI quality discipline;
- that automated evaluation replaces domain experts;
- that model scores prove safety;
- that the referenced open-source implementations are production-certified;
- that a single maturity model fits every organization.

AI Quality Engineering should evolve with the systems, standards and risks it evaluates.

---

## 50. Conclusion

AI changes software behavior from mostly deterministic execution into a system where code, data, retrieval, prompts, models, tools, identity and runtime context interact dynamically.

Quality Engineering must therefore evolve from validating features to engineering **evidence, controls and learning loops** across the complete AI system.

The AI Quality Engineer is the role proposed to lead that evolution.

The discipline can be summarized in six verbs:

> **Understand. Model. Evaluate. Control. Observe. Learn.**

The role succeeds when teams can answer, with evidence:

- What was expected?
- What actually happened?
- Was the evidence trustworthy?
- Was the action authorized?
- Did the system remain safe and reliable?
- Is the release risk acceptable?
- Will this failure be caught next time?

The final principle is:

> **AI quality is not confidence in a model. It is confidence in an evidence-backed engineering system that can detect, explain, control and learn from AI behavior.**

---

## References

1. NIST, *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*, NIST AI 600-1.
2. NIST, *AI Agent Standards Initiative*, 2026.
3. OWASP GenAI Security Project, *OWASP Top 10 for Agentic Applications 2026*.
4. OpenTelemetry, *Semantic Conventions* and Generative AI observability guidance.
5. Model Context Protocol, public protocol specifications and ecosystem guidance.
6. Ashok Kumar Manohar, open-source AI Quality Engineering reference implementations linked throughout this paper.

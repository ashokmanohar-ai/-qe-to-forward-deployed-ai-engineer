# Stage 4 — Forward Deployed Engineering

**Weeks 17-20 · Exit outcome:** discover, design, prototype, deploy, troubleshoot, and explain a realistic customer solution.

## Week 17: Discover the problem

Do not accept “build a chatbot” as a problem statement.

### Discovery sequence

1. **Outcome:** what business or user result should improve?
2. **Workflow:** who does what today, using which systems and decisions?
3. **Pain:** where are time, errors, risk, delay, or missed opportunity created?
4. **Baseline:** how often, how long, how costly, and how severe?
5. **Users:** who benefits, operates, approves, supports, or can be harmed?
6. **Data:** what exists, who owns it, how fresh/complete is it, and what is sensitive?
7. **Constraints:** identity, integration, policy, region, latency, budget, and timeline.
8. **Success:** what measurable change and minimum quality makes adoption rational?
9. **Non-goals:** what will the pilot explicitly not do?
10. **Rollout:** how will users review, override, escalate, and provide feedback?

### Discovery brief

Write two pages containing problem, users, current workflow, baseline, proposed hypothesis, alternatives (including non-AI), success metrics, constraints, risks, non-goals, unknowns, and the next evidence-generating step.

## Week 18: Design the smallest credible solution

Start with a vertical slice that touches the real data and integration boundaries but limits users, scope, data, and side effects.

Required artifacts:

- system context and container diagrams;
- successful and failure sequence diagrams;
- API/tool/data contracts;
- identity, authorization, and tenant boundary;
- source-of-truth and data-lifecycle map;
- evaluation and observability plan;
- threat model and risk register;
- ADRs for model, retrieval, integration, and deployment choices;
- assumptions with owners and due dates.

### Design review prompts

- Where can the system be confidently wrong?
- Which data can cross which boundary?
- What happens when every dependency is slow, unavailable, or inconsistent?
- Which decision is reversible and which creates lock-in?
- Where is human judgment required?
- How do we know the solution improved the workflow rather than shifted work?

## Week 19: Prototype with honesty

Time-box the riskiest assumptions first: access, data quality, retrieval, model behavior, integration, or latency.

### Prototype review

Separate three columns:

| Proven | Assumed | Required for production |
|---|---|---|
| Evidence from the vertical slice | Beliefs not yet tested | Security, scale, operations, governance, hardening |

Demo a normal case, an edge case, a deliberate failure, an abstention/escalation, and an operational trace. Report the evaluation dataset and known gaps before showing polished UI.

### Production plan

Define phases, owners, dependencies, acceptance gates, environments, data migration, security review, performance test, user acceptance, training, rollout, rollback, monitoring, support, and cost controls.

## Week 20: Troubleshoot and communicate

### Incident rhythm

1. confirm impact, scope, severity, start time, and affected segments;
2. establish an incident lead, investigation owners, and update cadence;
3. mitigate user impact with rollback, fallback, disablement, or capacity;
4. preserve deployments, config, prompts, model versions, traces, and samples;
5. build a timeline and test competing hypotheses;
6. verify recovery against user symptoms and quality metrics;
7. communicate confirmed facts, uncertainty, actions, and next update;
8. conduct a blameless review with owned corrective actions.

### Customer update template

> **Impact:** [who/what is affected and how].  
> **Current state:** [mitigated, ongoing, or recovered].  
> **What we know:** [confirmed evidence only].  
> **What we are doing:** [mitigation and investigation work].  
> **Customer action:** [required action or “none”].  
> **Next update:** [specific time].

Complete [Lab 8](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/08-production-incident).

## Stage review

Give a five-minute executive explanation, a 30-minute technical review, and a live incident walkthrough for the same solution. The content should change by audience; the underlying evidence must not.

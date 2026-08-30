# Lab 6 — Build a bounded API tool agent

## Scenario

An assistant can look up an order, estimate a refund, and create a support ticket. A retry creates two tickets and a crafted document attempts to instruct the agent to issue a refund.

## Tools

| Tool | Side effect | Required control |
|---|---|---|
| `lookup_order` | No | user/tenant authorization and field filtering |
| `estimate_refund` | No | deterministic policy version and explanation |
| `create_ticket` | Yes | idempotency key, confirmation, rate limit, audit |
| `issue_refund` | Yes/high risk | excluded from autonomous scope; human workflow only |

## Build

1. Define strict JSON schemas for tools.
2. Keep user identity outside model-controlled arguments.
3. Validate plan, tool name, arguments, authorization, budget, and step count.
4. Ask for explicit confirmation before `create_ticket`.
5. Generate an idempotency key tied to the approved action.
6. Execute with timeout and bounded retry.
7. Record request, policy decision, approval, tool result, and final response using safe fields.

## Adversarial tests

- unknown tool and extra argument;
- order belonging to another tenant;
- prompt/document requesting `issue_refund`;
- tool timeout after success but before response;
- repeated approval submission;
- loop attempting more than the step budget;
- result containing instruction-like text;
- user asks to reveal hidden configuration or another customer's data.

## Evidence

Agent traces for allowed, denied, confirmed, duplicated, timed-out, and recovered paths, plus a one-page side-effect policy.


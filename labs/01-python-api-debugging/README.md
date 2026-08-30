# Lab 1 — Repair a Python API client

## Context

A customer adapter intermittently fails. The current implementation retries every error, can return an uninitialized value, trusts malformed payloads, has no timeout contract, and provides no useful evidence.

## Task

Review `starter/broken_client.py` without running the solution first.

1. List every observable failure and hidden risk.
2. Define retryable versus terminal behavior.
3. Introduce typed models and specific exceptions.
4. Inject transport, retry delay, and observability dependencies.
5. Add tests for success, 404, 429 then success, repeated 503, timeout, malformed JSON shape, and invalid customer ID.
6. Compare your result with `solution/client.py` only after tests pass.

## Constraints

- maximum three attempts;
- never retry validation, authentication, authorization, or not-found errors;
- retry rate limit, timeout, and transient server errors only;
- preserve the original cause;
- do not log a full customer payload;
- no real network call is required.

## Failure injection

Add a fake transport returning: `429`, `503`, then `200`. Verify three attempts and one successful result. Then change the first response to `404` and verify exactly one attempt.

## Evidence

- failure inventory;
- implementation and tests;
- attempt log with safe fields;
- a short explanation of why “retry everything” can amplify an outage.


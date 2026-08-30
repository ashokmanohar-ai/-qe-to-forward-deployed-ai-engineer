# Lab 2 — Make a REST operation retry-safe

## Scenario

A customer UI creates a support case. The API processes the request, but the response is lost. The browser retries and creates a duplicate case.

## Build

Add `POST /v1/cases` to a small FastAPI service.

1. Require identity and tenant context.
2. Validate subject, description, priority, and length limits.
3. Require an `Idempotency-Key` header.
4. Store the key, normalized request hash, status, and response atomically.
5. Return the saved response for the same key and same request.
6. Return `409` if the same key is reused with a different request.
7. Return a machine-readable error with a correlation ID.

## Tests

- create succeeds with `201`;
- missing/invalid auth is `401`;
- wrong tenant is `403`;
- invalid request is `422`;
- same key and body returns the same case ID;
- same key and different body is `409`;
- two concurrent identical requests create one case;
- the idempotency record expires only according to a documented policy.

## Failure injection

Add a test transport that commits the database transaction and then raises a simulated connection reset before returning. Prove the client can retry without duplicate state.

## Customer explanation

Explain idempotency without using the word “idempotency”: “If the customer repeats the same request because they did not receive a response, the system returns the original result instead of doing the action twice.”


# Stage 1 — Foundation

**Weeks 1-5 · Exit outcome:** build, test, document, and debug a typed Python API backed by SQL.

This stage changes your center of gravity from “automate validation around a product” to “build and own a small product.” Keep your testing instincts, but design the service before writing its tests.

## Week 1: Python for builders

### Learn

- values, collections, control flow, functions, classes, dataclasses, and modules;
- type hints, protocols, dependency injection, context managers, and iterators;
- exceptions, logging, configuration, packaging, and command-line interfaces;
- unit versus integration tests and test doubles.

### Build

Complete [Lab 1](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/01-python-api-debugging), then add one customer API adapter to your capstone.

Use this order:

1. define the input/output contract with types;
2. isolate network I/O behind an interface;
3. classify errors as retryable or terminal;
4. add bounded retry with observable attempts;
5. test success, timeout, rate-limit, malformed response, and exhausted retry;
6. document why each exception is handled at that layer.

### Exit check

Can another engineer change the HTTP client without rewriting domain logic or tests? If not, separate transport from behavior.

## Week 2: Operate the runtime

Treat every command as an experiment: write a hypothesis, run the cheapest discriminating check, observe, and update the hypothesis.

### Request-path investigation

```bash
git status
git log --oneline --decorate -10
python --version
ps aux
ss -lntp                         # Windows: Get-NetTCPConnection
curl -v http://localhost:8000/health
curl -v --connect-timeout 2 https://example.com
```

Ask at each layer:

| Layer | Question | Evidence |
|---|---|---|
| Name resolution | Did the name resolve to the expected address? | DNS result and resolver configuration |
| Transport | Is the port reachable and accepting connections? | connection timing/error |
| TLS | Is trust, name, and validity correct? | certificate chain and hostname |
| HTTP | Did a proxy, gateway, or app return the response? | status, headers, correlation ID |
| Process | Is the expected version listening on the expected interface? | process, command, port binding |
| Application | Which dependency or code path failed? | structured logs and trace |

### Challenge

Run the service bound to `127.0.0.1`, then attempt to reach it from another container. Diagnose why a healthy local process is not externally reachable. Fix the binding deliberately and explain the security implication of `0.0.0.0`.

## Week 3: SQL and data quality

Create a SQLite schema for:

- tenants and users;
- documents and ingestion versions;
- conversations and requests;
- evaluation cases and results;
- customer feedback and incident links.

### Quality gates

Add checks for:

- entity uniqueness and referential integrity;
- required fields and allowed values;
- timestamps, freshness, and ordering;
- tenant ownership on every customer-scoped record;
- idempotent ingestion keys;
- row-count and distribution anomalies.

Complete [Lab 3](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/03-sql-data-pipeline). Do not “fix” duplicate ingestion with `SELECT DISTINCT`; identify identity and enforce it at the write boundary.

## Week 4: REST services

### Design the contract first

For each operation, define:

1. actor and authorization;
2. request and response schema;
3. validation and size limits;
4. idempotency and concurrency behavior;
5. status and machine-readable error codes;
6. timeouts, retry expectations, and rate limits;
7. logs, metrics, and audit fields;
8. versioning and compatibility.

Use the repository's reference API, then complete [Lab 2](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/02-rest-service).

### Required test matrix

| Area | Minimum cases |
|---|---|
| Contract | valid, missing, wrong type, extra field, boundary size |
| Identity | missing key, invalid key, revoked key |
| Authorization | allowed tenant, wrong tenant, restricted operation |
| Reliability | dependency timeout, retryable response, partial failure |
| Idempotency | same key/same request, same key/different request, concurrent repeat |
| Observability | correlation ID, safe log fields, latency and error metric |

## Week 5: Design before scaling

Model the service using four views:

- **Context:** users and external systems;
- **Container:** API, worker, database, vector store, model, and observability;
- **Sequence:** a successful request;
- **Failure sequence:** a slow or unavailable dependency.

Write two ADRs:

1. synchronous versus asynchronous ingestion;
2. relational database versus document/vector storage for each data type.

### System-design questions

- What state is authoritative?
- What can be recomputed?
- Which operations need strong consistency?
- What is safe to retry?
- Where do you apply backpressure?
- What is the blast radius of each dependency?
- What is the simplest acceptable degradation?

## Stage review

Demonstrate the service from a clean checkout. Then deliberately stop the database or adapter and show that errors are bounded, observable, and understandable. A reviewer should be able to find the contract, run tests, and explain the architecture in under 15 minutes.

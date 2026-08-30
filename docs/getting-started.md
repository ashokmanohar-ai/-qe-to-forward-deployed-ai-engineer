# Getting started

## Prerequisites

You need:

- Python 3.11 or newer;
- Git;
- Docker Desktop or Docker Engine;
- a code editor;
- 8-10 hours per week;
- one domain you understand well enough to identify realistic workflows and risks.

Kubernetes, Terraform, and a cloud account are not required on day one. Add them in Stage 2. Paid model access is optional; the reference implementation is deterministic and provider-neutral.

## Set up the repository

```bash
git clone https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer.git
cd -- -qe-to-forward-deployed-ai-engineer
python -m venv .venv
```

Activate the environment:

=== "macOS / Linux"

    ```bash
    source .venv/bin/activate
    ```

=== "Windows PowerShell"

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

Install and verify:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
fde-roadmap overview
make validate
make test
```

## Run the service locally

```bash
cp .env.example .env
# Replace the example local API key in .env.
docker compose up --build
```

Verify:

```bash
curl http://localhost:8000/health
curl -H "X-API-Key: <your-local-key>" http://localhost:8000/v1/status
```

Stop and clean up:

```bash
docker compose down
```

## Create an evidence branch

Use one branch per weekly outcome:

```bash
git switch -c week-01-python-api-client
```

A weekly pull request should contain:

1. the problem and acceptance criteria;
2. the implementation or analysis;
3. normal, boundary, and failure evidence;
4. security and operational considerations;
5. what you would change for production;
6. a customer-friendly explanation.

## Use the tracker

```bash
fde-roadmap next
fde-roadmap start 1
fde-roadmap complete 1 --evidence "PR #1 and docs/week-01-reflection.md"
fde-roadmap status
```

The CLI validates week numbers and prerequisites. It does not upload evidence or send data anywhere.

## Working without cloud credits

You can complete the core roadmap locally:

- use SQLite before managed SQL;
- use the deterministic vector store before a hosted vector database;
- use Docker Compose and a local Kubernetes distribution;
- use Terraform's Docker provider;
- design AWS/Azure/GCP alternatives using decision records;
- use recorded or synthetic customer data only.

When cloud access becomes available, deploy only one reference architecture deeply. The ability to explain boundaries and trade-offs matters more than creating three shallow deployments.

## Safety rules

- Never use real customer data, secrets, production credentials, or proprietary prompts.
- Do not run destructive tools or load tests against systems without written authorization.
- Treat retrieved documents, model outputs, and tool responses as untrusted input.
- Put side effects behind authorization, idempotency, limits, and human approval.
- Delete temporary cloud resources and confirm billing after each lab.


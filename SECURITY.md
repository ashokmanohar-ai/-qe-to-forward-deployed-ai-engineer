# Security Policy

## Supported version

The latest commit on `main` is supported. This repository is educational and is not a managed production service.

## Report a vulnerability

Do not open a public issue for a suspected vulnerability or exposed credential. Use GitHub's private vulnerability reporting feature when enabled, or contact the repository owner privately through the address on their GitHub profile.

Include the affected path, reproduction steps, impact, and a safe mitigation. Do not include real secrets, personal data, or customer data.

## Security assumptions

- The reference service uses an API key only to demonstrate an authentication boundary; production deployments should use an identity provider, short-lived tokens, and authorization policies.
- The in-memory vector store is for local learning. Production systems require durable storage, tenant-level access control, encryption, backups, and deletion workflows.
- Tool execution is allowlisted and bounded, but sample tools are non-transactional. Real side-effecting tools need idempotency, approval, authorization, rate limits, and audit logs.
- Never place provider keys in source, container images, Terraform state, logs, traces, prompts, or committed `.env` files.

See the production security stage and threat-model template before adapting this code.


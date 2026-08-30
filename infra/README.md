# Infrastructure examples

These examples teach delivery boundaries without requiring a paid cloud account.

- `kubernetes/` deploys the service with non-root security, probes, limits, autoscaling, and a default-deny network policy.
- `terraform/` uses the Docker provider to demonstrate plan/apply/state locally.

Before applying:

1. build and tag the image expected by the manifest or replace the image value;
2. create the Kubernetes secret out of band;
3. review every resource and destructive change;
4. use only local/sandbox infrastructure you are authorized to change;
5. destroy temporary resources and verify cleanup.

For cloud work, use modules and remote state with locking, short-lived identity, encryption, policy checks, protected environments, budgets, and explicit ownership. Do not place credentials or sensitive outputs in Terraform variables/state.


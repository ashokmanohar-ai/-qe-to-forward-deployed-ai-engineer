# Lab 4 — Diagnose a failing container deployment

## Scenario

Version `1.2.0` rolls out. Pods enter `CrashLoopBackOff`; after a quick “fix,” pods run but never become Ready. The service is unavailable.

## Injected faults

- required `FDE_API_KEY` Secret is missing;
- readiness probe points to an authenticated endpoint;
- memory limit is lower than the observed startup peak;
- the image listens on `127.0.0.1` in one variant;
- network policy blocks an external dependency in another variant.

## Investigation rules

Do not edit the deployment until you can state which evidence proves the current hypothesis.

Collect:

```bash
kubectl get deploy,rs,pod,svc,endpoints -n qe-fde-learning -o wide
kubectl describe pod <pod> -n qe-fde-learning
kubectl logs <pod> -n qe-fde-learning --previous
kubectl get events -n qe-fde-learning --sort-by=.lastTimestamp
kubectl get deploy qe-fde-ai -n qe-fde-learning -o yaml
```

## Deliverables

- hypothesis table: signal, possible cause, discriminating check, result;
- minimal mitigation and confirmed recovery;
- root cause versus contributing factors;
- corrected probes and resource settings;
- runbook entry and prevention action;
- customer update with impact and recovery time.

## Stretch

Use a canary deployment. Define an automatic rollback signal that includes both HTTP availability and task-quality smoke tests.


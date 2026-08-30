# Project 3 — Build an LLM evaluation framework

## Why this project matters

This is the most direct bridge from Quality Engineering into differentiated AI Engineering. The framework should answer: “Is this change safe and valuable for the users and segments that matter?”

## Capabilities

- versioned datasets and immutable run metadata;
- deterministic validators for schema, citations, policy, tools, latency, and budget;
- retrieval metrics such as recall@k and MRR;
- rubric-based model graders with calibrated human samples;
- pairwise and baseline comparison;
- segment analysis by intent, risk, tenant class, language, and complexity;
- critical cases that cannot be averaged away;
- confidence intervals or repeat-run variance where appropriate;
- CI release decision and machine-readable report;
- production-sample ingestion with redaction and governance.

## Data model

Track dataset/version, case ID, inputs, references, required/forbidden behavior, tags, evaluator/version, candidate configuration, raw output, raw evidence, score, pass/fail, latency, tokens, cost, trace ID, and reviewer decision.

## Acceptance criteria

- same inputs/configuration produce traceable, comparable run records;
- evaluator failures are not mistaken for application failures;
- protected-segment regression blocks release despite aggregate improvement;
- grader calibration includes agreement and disagreement examples;
- reports link scores to raw evidence and trace IDs;
- secrets and sensitive samples are excluded/redacted by policy.

## Interview story

Show a release the framework correctly blocked. Explain why the metric, threshold, segmentation, and evidence matched customer risk rather than being chosen after seeing results.


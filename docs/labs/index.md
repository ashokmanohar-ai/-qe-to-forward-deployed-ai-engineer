# Hands-on labs

Labs follow the same structure: **context → task → constraints → failure injection → verification → evidence → cleanup**.

| # | Lab | Primary outcome | Suggested week |
|---:|---|---|---:|
| 1 | [Python API debugging](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/01-python-api-debugging) | Reliable typed adapter | 1 |
| 2 | [REST service](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/02-rest-service) | Safe service contract | 4 |
| 3 | [SQL data pipeline](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/03-sql-data-pipeline) | Idempotent quality-gated ingestion | 3 |
| 4 | [Container debugging](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/04-container-debugging) | Evidence-led Kubernetes recovery | 6-7 |
| 5 | [RAG quality](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/05-rag-quality) | Retrieval and tenant-safety evaluation | 13-14 |
| 6 | [Agent tool calling](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/06-agent-tool-calling) | Bounded, idempotent tools | 15 |
| 7 | [Observability and evaluation](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/07-observability-evaluation) | Segment-aware release gate | 16/22 |
| 8 | [Production incident](https://github.com/ashokmanohar-ai/-qe-to-forward-deployed-ai-engineer/tree/main/labs/08-production-incident) | Mitigation, RCA, and communication | 20 |

## Lab evidence rubric

Score 0-2 for each area:

| Area | 0 | 1 | 2 |
|---|---|---|---|
| Reproducibility | cannot run | runs with missing steps | clean setup and cleanup |
| Correctness | happy path only | some failures tested | contract, boundaries, and failures proven |
| Diagnosis | guessed fix | partial evidence | hypotheses eliminated with evidence |
| Security | ignored | risks listed | boundaries tested and residual risk stated |
| Operations | no signals | logs only | correlated signals and recovery steps |
| Communication | code only | technical summary | customer impact plus technical explanation |

Target at least 10/12 before marking a lab complete.

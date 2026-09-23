# JEV RCA Studio

AI Failure Intelligence and Root Cause Analysis for Playwright test reports.

## Capabilities

- Upload Playwright JSON reports or ZIP files containing JSON reports
- Detect failed tests and extract error evidence
- Classify likely root cause:
  - Product defect
  - Automation issue
  - Environment issue
  - Flaky test
  - Test-data problem
- Optional JEV / TypeSafe AI-assisted RCA
- Front-end API key input; key is not persisted
- Health endpoint at `/health`

## Railway

Start command:

```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
```

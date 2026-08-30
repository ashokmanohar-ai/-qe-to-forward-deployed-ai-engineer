# Lab 3 — Stop silent duplicate ingestion

## Scenario

A document ingestion worker is retried after a timeout. The same source version is inserted twice, chunks are embedded twice, retrieval overweights that document, and cost increases.

## Task

Design tables for `tenant`, `source_document`, `document_version`, `chunk`, and `ingestion_run`.

The identity of a version is `(tenant_id, source_id, source_version)`. Enforce it in the database, not only application code.

## Steps

1. Load `events.csv` or create 100 synthetic events with intentional duplicates.
2. Profile nulls, uniqueness, ranges, timestamps, and tenant distribution.
3. Use a staging table and transactional merge/upsert.
4. Reject rows with missing tenant/source/version.
5. Record accepted, duplicate, rejected, and failed counts by run ID.
6. Re-run the same input and prove zero new versions/chunks are created.
7. Add a query that detects versions with missing or excessive chunks.

## Verification queries

```sql
SELECT tenant_id, source_id, source_version, COUNT(*)
FROM document_version
GROUP BY tenant_id, source_id, source_version
HAVING COUNT(*) > 1;
```

```sql
SELECT dv.id, dv.expected_chunk_count, COUNT(c.id) AS actual_chunk_count
FROM document_version AS dv
LEFT JOIN chunk AS c ON c.document_version_id = dv.id
GROUP BY dv.id, dv.expected_chunk_count
HAVING COUNT(c.id) <> dv.expected_chunk_count;
```

## Evidence

Schema, migration, quality queries, first-run report, replay report, and explanation of how duplicate chunks affect retrieval quality—not only storage.


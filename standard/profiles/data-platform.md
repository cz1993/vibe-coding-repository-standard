# Profile: Data Platform

## Select when

The repository primarily performs collection, ingestion, transformation, normalization, analytics, machine learning, data delivery, or scheduled data operations.

## Recommended shape

```text
src/                    # reusable domain/application code
pipelines/              # declarative definitions or thin orchestration entry points
sql/                    # version-controlled SQL grouped by owned concern
models/                 # analytical/ML model definitions when applicable
notebooks/              # controlled exploration or operational notebooks
tests/
migrations/
ops/ or infra/
docs/
scripts/
```

## Rules

- Production logic should move from notebooks into tested modules when it becomes recurring or critical.
- Every notebook declares `exploratory`, `operational`, or `generated` status and owner.
- Schedules, run IDs, idempotency, retries, overlap, partial failure, and reconciliation must be explicit for production pipelines.
- Raw evidence, normalized records, business evaluation, and client/external outputs should have versioned contracts where auditability matters.
- Time zones, currencies, units, null semantics, deduplication, and late-arriving behavior must be explicit.
- Database migrations and data backfills are distinct operations with validation and recovery plans.
- Client/tenant isolation must be tested at data access and output generation boundaries.

## Expected evidence

- pipeline/CLI/scheduler entry points;
- source-to-output lineage for critical flows;
- schema and file contract tests;
- fixture-based source/parsing edge cases;
- idempotency/retry/overlap tests;
- row-count/checksum/reconciliation evidence;
- data quality and delivery monitoring;
- backfill, failed-run, and restore runbooks.

## Anti-patterns

- scripts with business logic and no importable modules;
- “successful” runs that hide partial failure;
- documentation as the only source of a schedule or schema;
- production notebooks with undeclared manual steps;
- one global `utils.py` for unrelated data concerns.

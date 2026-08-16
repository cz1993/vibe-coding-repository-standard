# Profile: Single Application / Modular Monolith

## Select when

- the repository produces one primary deployable application or runtime;
- modules share a release/deployment lifecycle;
- a distributed service boundary is not operationally justified.

## Recommended shape

```text
src/ or framework-native source root/
tests/
migrations/             # when schema is owned here
ops/ or infra/          # runtime/deployment definitions
docs/
scripts/
```

## Boundary guidance

- Organize modules around business capabilities or cohesive change reasons.
- Keep external database, API, file, queue, clock, and UI details at testable boundaries where useful.
- Do not create `services/` folders that imply independent deployability when all modules run together.
- Use explicit internal contracts for important seams, not a network boundary by default.
- Keep entry-point scripts thin and application logic importable/testable.

## Expected evidence

- local/run/build/test commands;
- primary entry points;
- module/data-flow overview;
- database migration path where applicable;
- critical contract/integration/smoke tests;
- deployment and rollback runbook for production applications.

## Split trigger

Consider an independent service only when separate deployment, scaling, availability, security, ownership, or release cadence is demonstrated and the added network/operations cost is accepted.

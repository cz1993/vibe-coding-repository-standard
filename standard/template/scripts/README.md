# Scripts

Scripts are discoverable entry points, not a dumping ground for business logic.

Use verb-object naming and group scripts by purpose when the repository has enough scripts to justify categories.

Recommended verbs:

```text
verify inspect generate export import migrate backfill repair deploy rollback delete
```

Every retained script should expose or document:

- purpose and owner;
- caller or invocation method;
- inputs and environment;
- outputs and side effects;
- production safety and permissions;
- idempotency or rerun behavior;
- validation and exit codes.

Prefer thin scripts that invoke importable, tested application modules. One-off experiments should live outside production command paths and be deleted after their evidence/retention need ends.

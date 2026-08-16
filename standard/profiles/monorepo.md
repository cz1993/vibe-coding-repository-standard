# Profile: Monorepo

## Select when

- several applications or packages intentionally share one repository;
- shared tooling, atomic changes, or coordinated releases justify the topology;
- ownership and dependency direction can be made explicit.

## Recommended shape

```text
apps/                    # deployable applications
packages/                # reusable packages/libraries
tools/                   # repository build/development tooling
infra/                   # shared infrastructure composition
tests/ or app/package-local tests
docs/
```

## Rules

- `apps/` contains deployable products, not arbitrary modules.
- `packages/` contains code with real consumers; do not extract packages only to shrink files.
- `services/` is reserved for independently deployable/operated services.
- Declare dependency direction and prevent cycles with build/lint tooling when possible.
- Scope nested instructions and skills only when a subtree truly has different commands or safety boundaries.
- Use one owner per writable package/app during parallel agent work.

## Expected evidence

- workspace/package-manager commands;
- dependency graph or ownership map;
- affected-package test strategy;
- release/versioning model;
- cross-package contract tests for important boundaries;
- CI that avoids silently skipping impacted packages.

## Anti-patterns

- copying shared code between apps instead of using a proven shared package;
- placing all code in `packages/common` or `utils`;
- allowing every package to depend on every other package;
- independent agent edits to overlapping workspaces without worktrees and integration ownership.

# Contributing

## Before starting

- Read `AGENTS.md` and the applicable architecture, decision, contract, or runbook documents.
- Confirm the issue or task has a clear user outcome and acceptance criteria.
- Identify production, client-data, migration, deployment, and external-service boundaries.
- Use a dedicated branch or worktree.

## Change scope

Prefer one coherent, self-contained change. Do not combine broad formatting, dependency upgrades, file moves, behavior changes, and cleanup in one pull request.

A structural refactor should preserve behavior and have characterization or contract evidence. A behavior change should make the intended difference clear.

## Development

- Trace the current execution path before changing it.
- Reuse the current stack before adding dependencies or abstractions.
- Follow language/framework-native conventions.
- Add tests at the smallest level that provides credible evidence.
- Include higher-level coverage for important boundaries and user/operational flows.
- Update documentation when commands, contracts, decisions, or operations change.

## Pull request evidence

Use `.github/PULL_REQUEST_TEMPLATE.md`. Show material test cases with:

| Scenario | Setup/input | Expected | Actual | Evidence |
|---|---|---|---|---|
| Replace | Replace | Replace | Replace | Command/report |

List tests not run and why. Explain migration, deployment, rollback, security, and data impact where applicable.

## Review

The author may validate its own work, but a non-trivial change requires independent review. Reviewers prioritize correctness, security, data integrity, regressions, failure behavior, compatibility, and useful tests. Preference-only comments are non-blocking.

## Git and remote actions

Do not force-push shared branches, bypass protections, self-merge, or rewrite history without explicit repository authorization. Confirm the intended Git identity before pushing or opening a pull request.

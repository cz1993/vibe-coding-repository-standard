---
name: repository-bootstrap
description: Audit and establish or upgrade the canonical repository governance baseline. Use only when explicitly asked to bootstrap, standardize, or upgrade a repository; do not use for feature development or source-code restructuring.
---

# Repository Bootstrap

## Inputs

- target repository root;
- approved standard/kit path and version;
- mode: audit-only or audit-and-apply;
- Git action: none, commit, or explicitly authorized push/PR;
- optional project context.

## Constraints

- Audit before editing.
- Protect uncommitted work.
- Do not access production, client data, live databases, deployments, schedules, or paid external services.
- Do not move/rename application code, change dependencies, implement features, or perform broad cleanup.
- Do not enable memories, hooks, network access, MCP servers, or optional indexing tools.
- Preserve framework-native conventions and merge existing governance files carefully.

## Procedure

1. Read the approved canonical standard and bootstrap plan.
2. Inspect Git state and create a dedicated branch/worktree before writes.
3. Inventory the stack, layout, commands, entry points, tests, CI, documentation, scripts, and agent/tool configuration.
4. Select a project profile and risk class.
5. Verify candidate commands safely; never publish unrun commands as verified.
6. Produce a proposal listing facts, unknowns, files, exceptions, non-goals, and validation.
7. In apply mode, add the smallest compatible governance surface.
8. Run validator tests, the standard validator, and safe project checks.
9. Use the independent read-only reviewer.
10. Commit locally only when gates pass and report exact outcomes.

## Outputs

- selected profile and risk;
- governance diff;
- verified command register;
- standard manifest and exceptions;
- validator/test evidence;
- unresolved risks and placeholders;
- branch/commit/PR identifiers when applicable.

## Completion

Completion means baseline governance is safe and validated. It does not mean the application architecture or documentation is fully recovered.

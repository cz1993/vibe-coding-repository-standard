---
name: repository-hygiene
description: Perform a read-only evidence-based audit of stale docs, agent files, scripts, generated artifacts, duplicate code, and optional tools. Use only when explicitly asked for cleanup or governance review; do not delete or refactor during the audit.
---

# Repository Hygiene Audit

## Inputs

- repository root;
- audit scope;
- approved standard version;
- known production/scheduler/operator context, if safely available.

## Constraints

- Read-only by default.
- Do not access production or client data.
- Do not delete, move, rename, refactor, upgrade, or rewrite during the audit.
- Do not treat missing static references as proof of no external caller.
- Do not optimize for file-count reduction.

## Procedure

1. Inventory documentation, agent instructions, skills, custom agents, hooks, memory, MCP, scripts, generated output, tests, CI, deployment, and entry points.
2. For candidate stale items, check imports/callers, CLI registration, scheduler/CI, deployment/IaC, runbooks, operators, external integrations, and data/file side effects.
3. Classify each item:
   - keep;
   - merge;
   - move to an authoritative location;
   - generated;
   - superseded and safe to delete;
   - retention/archive required;
   - unknown and investigate.
4. Identify rules better enforced by tests/CI.
5. Identify context duplication and instruction precedence problems.
6. Produce a risk-ranked proposal with evidence and validation steps.

## Output

- inventory and classification;
- evidence for proposed removals;
- contradictions and unknowns;
- proposed small cleanup changesets;
- rules to convert into executable controls;
- expected context/maintenance improvement;
- items deliberately retained.

Deletion and refactoring require a separate reviewed change.

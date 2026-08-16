# Repository Instructions

## Mission

Replace this paragraph with a short, verified description of the product or system, its users, and the outcome this repository is responsible for. Do not paste a roadmap or historical narrative here.

## Sources of truth

Use this order when investigating behavior:

1. safe read-only runtime or deployed evidence, when explicitly available;
2. executable configuration, migrations, contracts, and tests;
3. current application code;
4. accepted architecture decisions and validated runbooks;
5. other current documentation;
6. historical files, generated summaries, transcripts, and legacy memory.

When sources disagree, report the conflict. Do not silently choose the most convenient source.

## Required workflow

Before editing:

1. identify the relevant entry point and callers;
2. trace inputs, outputs, dependencies, data access, external calls, and side effects;
3. identify existing tests or define a characterization approach;
4. state the smallest proposed change and acceptance criteria;
5. keep structural refactors separate from behavior changes where practical.

During implementation:

- solve the current demonstrated problem;
- reuse existing project code, language/runtime facilities, platform features, and installed dependencies before adding abstractions;
- keep unrelated files untouched;
- do not add speculative frameworks, services, extension systems, or dependencies;
- do not weaken validation, security, privacy, tenant isolation, error handling, observability, accessibility, migrations, recovery, or useful tests in the name of minimalism;
- preserve backward-compatible data, API, file, and operational contracts unless the task explicitly authorizes a migration;
- prefer reversible changes.

Before completion:

- run relevant safe validation;
- review the complete diff;
- confirm no secrets, client data, generated logs, or unrelated changes were added;
- use independent review for non-trivial work;
- update authoritative docs only when a command, contract, decision, or operating procedure changed.

## Verified commands

This section may contain only commands that have been executed successfully in this repository. Add the real commands during bootstrap and remove this placeholder.

```text
No verified commands recorded yet.
```

The detailed command register is `docs/reference/commands.md`.

## Test and pull-request evidence

For each material scenario, the implementation handoff and pull request must show:

- scenario or risk;
- setup/input;
- expected result;
- actual result;
- command, output, screenshot, or report evidence.

State which relevant tests were not run and why. “Tests pass” without commands or outcomes is not enough. Generated tests must be reviewed for whether they would fail when the behavior is broken.

## Safety boundaries

Without explicit authorization, do not:

- access or mutate production systems;
- use production or client credentials;
- deploy, migrate, roll back, delete data, or change schedules;
- call paid, rate-limited, or live external services;
- expose secrets, personal data, or client data;
- perform destructive Git, cloud, database, or filesystem operations;
- push, open, approve, merge, or bypass protections on remote changes.

Use synthetic or properly sanitized fixtures. Keep read and write capabilities separate.

## Agent and tool governance

- Keep this file concise; focused workflows belong in skills and detailed knowledge belongs in authoritative docs.
- Do not create active alternative instruction or memory files.
- Nested `AGENTS.md` or `AGENTS.override.md` files require an explicit manifest allowlist and a narrow scope.
- Memories and hooks remain disabled unless separately admitted.
- MCP servers and external tools require a documented least-privilege admission.
- The executor must not independently approve its own change.
- The reviewer reports findings and remains read-only unless the task explicitly assigns a different role.
- Do not commit agent transcripts, scratchpads, generated reasoning summaries, or task prompts as project documentation.

## Communication

Use plain, direct, user-friendly language. Explain unavoidable jargon. Distinguish confirmed facts, evidence-backed inferences, and unknowns. Report actual validation results and material uncertainty; do not overstate completion.

## Focused references

- Documentation map: `docs/README.md`
- Architecture: `docs/architecture/README.md`
- Decisions: `docs/decisions/`
- Operations: `docs/runbooks/`
- Commands/contracts: `docs/reference/`
- Contribution and review: `CONTRIBUTING.md`
- Security: `SECURITY.md`

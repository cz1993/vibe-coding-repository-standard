# Vibe Coding Repository Standard — Normative Specification

**Standard ID:** VCRS-1  
**Status:** Public preview normative specification  
**Version:** 0.1.0  
**Date:** 2026-08-15

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** express requirement strength.

## 1. Purpose

This standard defines a predictable operating surface for human- and agent-assisted software development across multiple repositories. It standardizes governance, discoverability, evidence, review, documentation, and safety while preserving language-, framework-, and domain-specific architecture.

It is designed for both new repositories and existing repositories that cannot safely be reorganized in one pass.

## 2. Governing principles

The repository MUST optimize in this order:

1. correctness, security, privacy, and data integrity;
2. preservation of explicit behavior and contracts;
3. understandable and reversible changes;
4. operational reliability and observability;
5. simple separation of concerns;
6. reuse after repeated evidence;
7. extensibility at known variation points;
8. performance supported by measurement.

Minimalism MUST NOT remove validation, error handling, migrations, tests, access controls, auditability, recovery paths, or contractual evidence.

## 3. Mandatory repository governance core

A compliant repository MUST contain or explicitly exempt the following:

```text
<repo-root>/
├── README.md
├── AGENTS.md
├── .repo-standard.json
├── .codex/
│   ├── config.toml
│   └── agents/
│       ├── repo-explorer.toml
│       ├── executor.toml
│       └── reviewer.toml
├── .agents/
│   └── skills/
│       ├── repository-bootstrap/
│       ├── safe-change/
│       └── repository-hygiene/
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── repository-standard.yml
├── docs/
│   ├── README.md
│   ├── architecture/
│   ├── decisions/
│   ├── runbooks/
│   └── reference/
├── scripts/
│   ├── README.md
│   └── maintenance/
│       └── validate_repository_standard.py
└── tests/
    └── standards/
```

An existing repository MAY use equivalent established locations when moving them would create more risk than value. The exception MUST be recorded in `.repo-standard.json` with its rationale and mapped path.

`CONTRIBUTING.md` and `SECURITY.md` are REQUIRED for repositories with multiple contributors, production responsibilities, client data, public exposure, or external vulnerability reporting. They are RECOMMENDED otherwise.

## 4. Project profiles

Every repository MUST select one primary profile in `.repo-standard.json`. It MAY select secondary profiles.

### 4.1 `single-application`

Use for one deployable application or a modular monolith.

Recommended shape:

```text
src/ or <language-native-source-root>/
tests/
migrations/             # when a database schema is owned here
ops/ or infra/          # deployment and runtime definitions
```

Modules SHOULD align to business capabilities rather than technical layers alone. External I/O SHOULD be separated from core business rules where doing so improves testability and change isolation.

### 4.2 `monorepo`

Use when multiple packages or applications intentionally share one repository.

Recommended shape:

```text
apps/                   # deployable applications
packages/               # reusable packages or libraries
tools/                  # repository build/development tooling
infra/                   # shared infrastructure definitions
```

Use `services/` only for independently deployable and independently operated services. A folder name MUST NOT imply a distributed architecture that does not exist.

### 4.3 `data-platform`

Use for collection, ingestion, transformation, analytics, or machine-learning workflows.

Recommended shape:

```text
src/                    # reusable application and pipeline code
pipelines/              # declarative pipeline definitions or thin entry points
sql/                    # version-controlled SQL grouped by owned concern
models/                 # analytical/model definitions when applicable
notebooks/              # exploration or controlled operational notebooks
tests/
migrations/
```

Production logic SHOULD migrate from notebooks into tested modules. Notebooks MUST declare whether they are exploratory, operational, or generated. Production data contracts and schedules MUST be executable or testable, not documented only in prose.

### 4.4 `infrastructure`

Use for infrastructure-as-code or platform configuration.

Recommended shape:

```text
modules/                # reusable infrastructure modules
environments/           # environment composition, not secret values
policies/               # policy-as-code
scripts/                # thin operator entry points
tests/                  # static, policy, plan, and integration tests
```

Secrets MUST NOT be committed. Environment directories SHOULD contain composition and references rather than copied modules.

## 5. Naming standard

### 5.1 Reserved canonical files

Use exact casing for:

```text
README.md
AGENTS.md
CONTRIBUTING.md
SECURITY.md
LICENSE
CHANGELOG.md
CODEOWNERS
```

Do not create active alternatives such as `agent.md`, `AGENT.md`, `instructions.md`, `memory.md`, or `readme-new.md`.

### 5.2 Directories and documentation

- General directories and Markdown documents MUST use `kebab-case` unless a framework requires another form.
- Architecture decision records MUST use `NNNN-short-decision-title.md`.
- Runbooks SHOULD use an action or event name, such as `recover-failed-run.md` or `rotate-api-key.md`.
- Generated files MUST be visibly marked and written to a documented generated-artifact location.
- Do not use catch-all active directories named `misc`, `stuff`, `other`, `archive`, `old`, `new`, `temp`, `final`, or `v2` without a defined domain or version contract.

### 5.3 Source code

Source names MUST follow the language and framework's established conventions. Examples:

- Python modules and scripts: `snake_case.py`;
- TypeScript/JavaScript components: project convention, consistently applied;
- classes/types: language-native type naming;
- tests: framework-native naming and placement, ideally mirroring the source concern.

The standard MUST NOT override a well-established framework convention merely for visual uniformity.

### 5.4 Scripts and commands

Human-invoked commands SHOULD use verb-object naming. The first verb SHOULD communicate risk and intent:

```text
verify-*
generate-*
inspect-*
export-*
import-*
migrate-*
backfill-*
repair-*
deploy-*
rollback-*
delete-*
```

A retained script MUST document:

- purpose and owner;
- caller or invocation method;
- required inputs and environment;
- outputs and side effects;
- production safety characteristics;
- idempotency or rerun behavior;
- validation method.

Business logic MUST NOT live only in opaque shell or one-off scripts when it belongs in importable, testable modules.

## 6. Sources of truth

Each repository MUST define its source-of-truth order in `AGENTS.md`. The default is:

1. observed runtime and deployed configuration, accessed safely and read-only;
2. executable configuration, migrations, contracts, and tests;
3. current application code;
4. accepted architecture decisions and validated runbooks;
5. other current documentation;
6. historical files, generated summaries, transcripts, and legacy memory.

When sources conflict, agents MUST report the conflict and collect evidence. They MUST NOT silently select the most convenient source.

## 7. `AGENTS.md` standard

The root `AGENTS.md` MUST contain only information useful to nearly every task in the repository:

- product/repository mission;
- source-of-truth order;
- verified commands;
- required change workflow;
- safety and production boundaries;
- testing and pull-request evidence requirements;
- communication requirements;
- links to focused authoritative documents.

It MUST NOT contain:

- full architecture reference material;
- current sprint or task status;
- long troubleshooting history;
- generated repository summaries;
- copied chat transcripts;
- secrets or client data;
- automatically appended lessons;
- rules already enforced adequately by deterministic tooling.

Recommended size is 4–8 KiB. The default hard budget is 16 KiB, enforced by the standard validator. A larger file requires a documented exception.

Nested `AGENTS.md` or `AGENTS.override.md` files MUST be explicitly allowlisted in `.repo-standard.json`, with scope and owner. Unknown nested instruction files are validation errors in strict mode.

Agent-facing communication MUST use plain, direct, user-friendly language. Unavoidable domain terminology SHOULD be explained when first used. Agents MUST distinguish confirmed facts, evidence-backed inferences, and unknowns.

## 8. Codex configuration standard

The initial project configuration SHOULD use:

- `approval_policy = "on-request"`;
- `sandbox_mode = "workspace-write"`;
- outbound network disabled in the workspace sandbox;
- no fallback agent-instruction filenames;
- a bounded `AGENTS.md` byte limit;
- memories disabled;
- hooks disabled;
- multi-agent support enabled with modest concurrency.

A project MUST NOT pin a model in the canonical template unless the repository has an approved, tested reason. Model selection changes more frequently than repository governance.

Project configuration MUST be reviewed before the repository is marked trusted. MCP servers, hooks, and external tools MUST be absent from the initial baseline unless an admission record has been approved.

## 9. Skills standard

Root skills MUST be narrowly scoped, have explicit inputs and outputs, and state when they must not run. Each skill MUST contain a valid `SKILL.md` with unique `name` and concise `description` metadata.

The initial universal root skills are:

| Skill | Invocation | Purpose |
|---|---|---|
| `repository-bootstrap` | Explicit only | Audit and establish the governance baseline |
| `safe-change` | May be implicit | Trace, plan, implement, validate, and report one bounded change |
| `repository-hygiene` | Explicit only | Read-only identification of stale, redundant, generated, or dangerous artifacts |

Do not add a new root skill until:

1. the workflow has repeated at least twice or is contractually critical;
2. its trigger and non-trigger cases are documented;
3. it cannot be expressed more simply in existing instructions;
4. it has an owner and maintenance cadence;
5. it does not duplicate another active skill.

Project- or module-specific skills SHOULD live at the narrowest applicable repository scope.

## 10. Multi-agent standard

The default roles are:

- **orchestrator:** owns task contract, decomposition, integration, and final decision;
- **repo explorer:** read-only mapping and evidence gathering;
- **executor:** implements one bounded change and provides test evidence;
- **reviewer:** read-only independent review for correctness, security, regression, and missing tests;
- **specialist:** optional, bounded domain expertise such as database, UI, or infrastructure review.

The executor MUST NOT issue the final independent approval of its own change. The reviewer SHOULD NOT edit the implementation. One agent MUST own each writable file set at a time. Concurrent work MUST use separate branches or worktrees unless the scopes cannot conflict.

Agent communication MUST use the structured handoffs defined in `05-multi-agent-development-protocol.md`. Agent transcripts and internal scratchpads MUST NOT be committed as project documentation.

## 11. Change and review standard

Each pull request SHOULD represent one coherent, self-contained change. Structural changes and behavior changes SHOULD be separated when practical.

Before editing, the executor MUST:

1. identify the relevant entry point and callers;
2. trace inputs, outputs, dependencies, and side effects;
3. identify existing tests or a characterization approach;
4. state the smallest proposed change;
5. define acceptance criteria.

The pull request MUST include test evidence in plain language. For each material scenario, show:

| Field | Required content |
|---|---|
| Scenario | Behavior or risk being verified |
| Setup/input | Fixture, state, or user action |
| Expected result | What should happen |
| Actual result | What happened |
| Evidence | Command, output, screenshot, or report reference |

“No tests” is acceptable only with a specific reason, risk assessment, and alternative validation. Generated tests MUST be reviewed for whether they would fail when the behavior is broken.

Reviewers MUST prioritize design fit, correctness, user impact, security, privacy, data integrity, concurrency, error handling, compatibility, migration safety, observability, and useful tests. Style-only comments MUST NOT block a change unless they reveal a real maintainability or correctness problem.

## 12. Documentation standard

The active documentation tree uses four purposes:

```text
docs/architecture/     # system explanation and boundaries
docs/decisions/        # why durable choices were made
docs/runbooks/         # operational procedures
docs/reference/        # exact commands, contracts, schemas, APIs
```

Tutorial or onboarding material MAY be added when it serves a real audience.

Each authoritative document SHOULD declare:

```text
Status: Draft | Authoritative | Superseded | Generated
Owner: <role or team>
Last validated: YYYY-MM-DD
Validated by: <tests, config, commands, or evidence>
Supersedes: <optional path or ADR>
```

A recent date alone does not prove accuracy. Link documents to executable evidence wherever possible.

Superseded active documentation SHOULD be deleted after its replacement is accepted. Git history is the default archive. A separate archive is permitted only for contractual, legal, client, incident, or audit evidence and MUST be excluded from normal agent instruction discovery.

## 13. Security and environment standard

Without explicit authorization, agents MUST NOT:

- access or mutate production systems;
- use production or client credentials;
- deploy, migrate, roll back, delete, or change schedules;
- expose client, personal, or secret data;
- call costly or rate-limited external services;
- alter remote repositories or branch protections;
- perform destructive Git or filesystem operations.

Production-affecting tools MUST be separately permissioned, explicit, auditable, and reversible. Read and write capabilities SHOULD be separated. Test fixtures MUST be synthetic or properly sanitized.

## 14. MCP, memory, and hooks standard

MCP servers, memories, and hooks are optional capabilities, not baseline requirements.

An MCP server requires an admission record documenting:

- concrete problem solved;
- data and environments accessed;
- authentication and permission scopes;
- tool inventory and read/write classification;
- approval behavior;
- context cost and expected output size;
- audit logging;
- failure and uninstall procedure;
- owner and review date.

Start with the narrowest read-only tools. Load or connect capabilities only when needed. Broad tool catalogs MUST NOT be exposed merely because they are available.

Memories MUST NOT be the sole source of team or project requirements. Hooks MUST NOT inject large narrative context or make hidden project changes. Both remain disabled until the repository is stable and their measured benefit exceeds their maintenance and trust cost.

## 15. Standard manifest

`.repo-standard.json` MUST record:

- standard version;
- primary and secondary profiles;
- `AGENTS.md` byte budget;
- active skills;
- approved nested agent files;
- admitted MCP servers;
- documented path exceptions;
- governance owner;
- last review date.

The manifest is not a substitute for project configuration. It is the validator's declaration of intended compliance.

## 16. Compliance levels

| Level | Meaning |
|---|---|
| Baseline | Governance files exist, configuration is safe, and the validator passes without errors |
| Operational | Verified commands, tests, runbooks, and ownership exist for normal operation |
| Managed | Independent review, branch protections, maintenance cadence, and optional tool admissions are active |

A repository MUST reach Baseline before the standard is called installed. Production repositories SHOULD reach Operational. Client-facing and business-critical repositories SHOULD reach Managed.

## 17. Exceptions

An exception MUST include:

- requirement being waived;
- reason and evidence;
- risk and mitigating control;
- owner;
- expiry or review date.

Exceptions MUST NOT be used to preserve undocumented behavior indefinitely.

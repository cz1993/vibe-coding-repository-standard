# Universal Codex Project Bootstrap Plan

**Purpose:** Let Codex establish the repository standard in any one project with minimal manual setup.  
**Default mode:** audit, propose, apply compatible governance changes, validate, and commit locally.  
**Safety default:** no production access, deployment, remote writes, or application-code restructuring.

## Inputs

Codex receives:

```text
PROJECT_ROOT=<absolute path>
STANDARD_KIT_PATH=<absolute path to this kit or standards repository>
MODE=audit-only | audit-and-apply
GIT_ACTION=none | commit | push-and-pr
STANDARD_VERSION=<version or latest approved local version>
PROJECT_CONTEXT=<optional short description>
```

Recommended default:

```text
MODE=audit-and-apply
GIT_ACTION=commit
```

`push-and-pr` requires explicit authorization and a verified remote/identity.

## Stage 0 — Safety and repository state

Codex must:

1. resolve and remain inside `PROJECT_ROOT`;
2. confirm whether it is a Git repository;
3. record current branch, commit, remotes, and dirty state;
4. refuse destructive cleanup of uncommitted work;
5. inspect repository-local `.codex`, `AGENTS*`, skills, hooks, and MCP configuration before trusting them;
6. identify likely secret files without reading or displaying secret values;
7. avoid production credentials, live databases, deployments, schedulers, and client data;
8. create a dedicated branch or worktree before applying changes.

Suggested branch:

```text
chore/repository-standard-bootstrap
```

For an untrusted or highly complex repository, use a separate clean worktree.

## Stage 1 — Read-only discovery

Codex must inventory:

- language(s), framework(s), package manager(s), and runtime(s);
- build, test, lint, type-check, format, migration, and local-run commands;
- application and operational entry points;
- existing source/test/docs/scripts/infra layout;
- CI and deployment definitions;
- current agent instruction chain and nested overrides;
- current skills, custom agents, hooks, memory, and MCP declarations;
- documentation status and likely sources of truth;
- repository risk class and likely project profile;
- existing naming conventions that should be preserved.

Commands copied from documentation are **candidate commands** until executed successfully. Codex must not place unverified commands into `AGENTS.md` or the README.

## Stage 2 — Classify the repository

Select one primary profile:

```text
single-application
monorepo
data-platform
infrastructure
```

Record secondary profiles only when they materially affect structure or validation.

Classify the bootstrap risk:

| Risk | Typical characteristics | Bootstrap behavior |
|---|---|---|
| Low | small, clean, tested, no production coupling | Apply full compatible core |
| Medium | active app, mixed docs/scripts, some missing tests | Apply governance only; note gaps |
| High | production/client data, unclear entry points, legacy/lite split, dirty state | Audit first; minimal or no writes |

Codex must explain the selected profile and any path exceptions in plain language.

## Stage 3 — Produce the bootstrap proposal

Before editing, create a concise plan containing:

- confirmed facts and evidence;
- unknowns and conflicting sources;
- selected profile;
- files to add, merge, leave unchanged, or deprecate;
- proposed `AGENTS.md` content and byte budget;
- verified commands;
- selected skills and custom-agent roles;
- proposed standard-manifest exceptions;
- validation commands;
- explicit non-goals.

The proposal must state that application-code moves, broad renames, dependency upgrades, framework changes, and feature work are out of scope.

## Stage 4 — Apply the governance baseline

When `MODE=audit-and-apply`, Codex should add or carefully merge:

```text
.repo-standard.json
AGENTS.md
.codex/config.toml
.codex/agents/repo-explorer.toml
.codex/agents/executor.toml
.codex/agents/reviewer.toml
.agents/skills/repository-bootstrap/
.agents/skills/safe-change/
.agents/skills/repository-hygiene/
.github/PULL_REQUEST_TEMPLATE.md
.github/workflows/repository-standard.yml
docs/README.md
docs/architecture/README.md
docs/decisions/0000-template.md
docs/runbooks/README.md
docs/reference/commands.md
scripts/README.md
scripts/maintenance/validate_repository_standard.py
tests/standards/test_validate_repository_standard.py
```

Rules:

- Merge; do not overwrite meaningful existing content blindly.
- Preserve existing framework-native paths.
- Do not create empty application directories merely to match a diagram.
- Do not duplicate existing PR templates, CI, security policies, or validators; integrate them.
- Do not activate MCP servers, memories, hooks, or network access.
- Do not add a model pin by default.
- Use placeholders only where an owner must fill a real project-specific value, and list every placeholder in the final report.
- Keep generated audit output in a gitignored temporary location.

## Stage 5 — Build the project-specific `AGENTS.md`

The file must be concise and contain:

1. repository mission;
2. source-of-truth order;
3. current architectural direction at a high level;
4. verified commands only;
5. change workflow;
6. safety/production boundaries;
7. test and PR evidence requirements;
8. communication rules;
9. links to focused docs.

Do not copy the entire canonical standard into the project file.

For an existing repository, inspect all `AGENTS.md`, `AGENTS.override.md`, and fallback instruction files along the root-to-working-directory path. Remove or rename stale alternatives only after their unique current requirements have been reconciled. Unknown nested instruction files must be surfaced, not silently ignored.

## Stage 6 — Validate

Run, where applicable:

1. repository-standard unit tests;
2. the standard validator;
3. project formatter/linter/type checker;
4. fast project tests;
5. relevant integration or smoke tests that are safe locally;
6. secret and tracked-artifact checks already used by the project.

Do not run tests that trigger production, paid external APIs, live external-service collection, destructive migrations, or external delivery without authorization.

Review the complete diff and confirm:

- no application behavior changed;
- no secrets or client data were added;
- no existing files were overwritten unintentionally;
- no stale agent file remains active without disposition;
- no optional tool was enabled;
- the README and `AGENTS.md` contain only verified commands;
- all standard exceptions are explicit.

## Stage 7 — Independent review

Use the read-only reviewer custom agent. The reviewer must examine:

- unintended behavior or configuration changes;
- unsafe privileges or network access;
- instruction precedence and context pollution;
- misleading commands or documentation;
- duplicate skills or agent roles;
- validator gaps and false confidence;
- tracked generated/log/secret-like files;
- whether the bootstrap overreached into architecture refactoring.

The executor resolves accepted findings. The reviewer rechecks the final diff. The orchestrator decides whether acceptance criteria are met.

## Stage 8 — Commit and report

When `GIT_ACTION=commit`, create a local commit such as:

```text
chore(repo): establish repository standard baseline
```

Do not push unless `GIT_ACTION=push-and-pr` was explicitly authorized.

The final report must contain:

- selected profile and risk class;
- files added, changed, and intentionally untouched;
- verified commands;
- tests and actual outcomes;
- agent/skill/MCP state;
- exceptions and unresolved risks;
- deprecated files requiring later review;
- recommended next change, limited to one coherent step;
- commit hash, if created.

## New repository variation

For a new empty repository, Codex may instantiate the applicable template more directly. It still must:

- select a profile;
- remove irrelevant placeholders;
- avoid unneeded empty directories;
- verify the template validator;
- record project-specific ownership and safety boundaries;
- avoid installing optional external tooling.

## Existing repository variation

For an existing repository, the first bootstrap is governance-only. Source layout standardization becomes a separate plan and pull request after:

- entry points and callers are known;
- tests or characterization exist;
- deployment and scheduling consumers are known;
- the intended module boundaries have been accepted;
- the move can be made without mixing behavior changes.

## Definition of done

The bootstrap is complete when:

- the repository passes baseline validation;
- the effective agent instruction chain is understood;
- a fresh agent can find verified commands and safety limits;
- the selected profile and exceptions are recorded;
- the executor/reviewer separation is configured;
- no optional high-context or high-privilege capability was enabled by default;
- the diff is limited to repository governance;
- the final report distinguishes verified facts, gaps, and recommendations.

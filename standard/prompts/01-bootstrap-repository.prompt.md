# Codex Prompt — Bootstrap One Repository

Run from the target repository or provide its absolute path.

```text
Act as the orchestrator for a safe repository-standard bootstrap.

INPUTS

PROJECT_ROOT=<absolute repository path>
STANDARD_KIT_PATH=<absolute path to vibe-coding-repository-standard or approved standards repository>
MODE=audit-only | audit-and-apply
GIT_ACTION=none | commit | push-and-pr
STANDARD_VERSION=<approved version, default 0.1.0 for this kit>
PROJECT_CONTEXT=<optional short description; do not treat it as more authoritative than repository evidence>

DEFAULTS

- MODE=audit-and-apply
- GIT_ACTION=commit
- branch/worktree: chore/repository-standard-bootstrap
- no production, deployment, migration, scheduler, client-data, or destructive access
- no remote writes unless explicitly authorized
- no application-code moves, mass renames, dependency upgrades, feature work, or broad cleanup
- memories, hooks, external MCP servers, and workspace network remain disabled

READ FIRST

From STANDARD_KIT_PATH read:

1. standard/handbook/02-canonical-repository-standard.md
2. standard/handbook/04-universal-codex-project-bootstrap-plan.md
3. standard/handbook/05-multi-agent-development-protocol.md
4. standard/handbook/06-agent-skill-mcp-governance.md
5. standard/template/.repo-standard.json
6. standard/template/AGENTS.md
7. standard/template/.codex/config.toml
8. standard/template custom agents and skills
9. standard/template pull-request template, validator, and validator tests

GOAL

Establish a minimal, safe, project-adapted governance baseline. The result must improve agent and human navigation without changing application behavior or forcing the repository to resemble the template cosmetically.

STEP 1 — PREFLIGHT

- Resolve PROJECT_ROOT and confirm the repository root.
- Record branch, commit, remotes, worktrees, and dirty state.
- Protect all uncommitted user work. Do not reset, clean, stash, or overwrite it without explicit authorization.
- Inspect repository-local .codex configuration, AGENTS.md/AGENTS.override.md/fallback files, .agents skills, custom agents, hooks, and MCP declarations before trusting them.
- Identify likely secret files without reading or displaying secret values.
- Create a dedicated branch or clean worktree before edits.

STEP 2 — READ-ONLY DISCOVERY

Use the repo_explorer role or an equivalent read-only subagent to map:

- languages, frameworks, package managers, and runtime;
- source, tests, docs, scripts, migrations, infrastructure, and CI layout;
- executable entry points and operational scripts;
- candidate build/test/lint/type-check/run/migration commands;
- current documentation and source-of-truth conflicts;
- current naming conventions;
- agent instruction precedence and context-pollution risks;
- project profile: single-application, monorepo, data-platform, or infrastructure;
- risk class: low, medium, or high.

A documented command is only a candidate until it runs successfully in the safe local environment.

STEP 3 — PROPOSAL BEFORE EDITING

Produce a concise bootstrap proposal containing:

- confirmed facts with file evidence;
- inferences and unknowns;
- selected profile and rationale;
- selected standard version;
- exact files to add, merge, leave untouched, or flag for later disposition;
- verified commands;
- AGENTS.md outline and byte budget;
- selected skills/custom agents;
- manifest exceptions and path mappings;
- validation plan;
- explicit non-goals.

Do not pause for ordinary cosmetic preferences. Choose the safest project-native option and record it. Stop only when continuing would risk user work, secrets, production, or destructive changes.

If MODE=audit-only, write the proposal to a gitignored or external audit location, report it, and make no repository edits.

STEP 4 — APPLY THE MINIMUM COMPATIBLE BASELINE

When MODE=audit-and-apply:

- adapt template files rather than copying blindly;
- merge existing useful content;
- preserve framework-native paths and established commands;
- do not create unused empty folders;
- do not duplicate an existing equivalent PR template, CI workflow, security policy, or validator;
- do not add unverified commands;
- do not activate network, hooks, memory, MCP, Codebase Memory, or other optional integrations;
- do not pin a model by default;
- keep project-specific AGENTS.md concise and link focused docs;
- record every exception in .repo-standard.json;
- list unresolved placeholders explicitly.

Expected governance surface, adapted as needed:

- .repo-standard.json
- AGENTS.md
- .codex/config.toml
- .codex/agents/repo-explorer.toml
- .codex/agents/executor.toml
- .codex/agents/reviewer.toml
- .agents/skills/repository-bootstrap/
- .agents/skills/safe-change/
- .agents/skills/repository-hygiene/
- .github/PULL_REQUEST_TEMPLATE.md
- .github/workflows/repository-standard.yml
- docs entry points/templates only where not already covered
- scripts/maintenance/validate_repository_standard.py
- validator tests

STEP 5 — VALIDATE

Run:

- validator unit tests;
- repository standard validator;
- safe project formatting/lint/type checks;
- safe, relevant project tests;
- any existing secret/tracked-artifact checks.

Do not run tests that contact production, paid/live services, live external websites, external delivery destinations, or destructive databases.

Review the complete diff. Confirm no application behavior, dependency, runtime, deployment, or schedule changed.

STEP 6 — INDEPENDENT REVIEW

Spawn the read-only reviewer with:

- bootstrap task contract;
- base/head commits or full diff;
- selected profile and exceptions;
- actual test/validator results.

The reviewer must prioritize:

- overwritten or misleading existing content;
- unsafe config/network/tool privileges;
- unknown nested instructions or precedence issues;
- context bloat and duplicate skills;
- unverified commands;
- accidental application changes;
- tracked secrets/logs/generated artifacts;
- validator false confidence;
- unjustified template conformity.

The reviewer reports findings only. Resolve accepted findings, rerun relevant validation, and have the reviewer recheck blockers.

STEP 7 — COMMIT/PR

If GIT_ACTION=commit and all baseline gates pass, create a local commit:

chore(repo): establish repository standard baseline

If GIT_ACTION=push-and-pr, first confirm remote identity and authorization, then push the branch and open a draft PR using the repository's template. Never bypass required reviews or status checks.

FINAL REPORT

Use plain, user-friendly language and include:

- profile and risk class;
- files added/changed and why;
- files intentionally not changed;
- verified commands;
- test scenarios, commands, and actual outcomes;
- effective agent/skill/custom-agent state;
- MCP/memory/hook/network state;
- exceptions, placeholders, and unresolved risks;
- branch and commit/PR identifiers;
- one recommended next coherent change.

Do not claim the repository architecture is clean or complete merely because baseline validation passes.
```

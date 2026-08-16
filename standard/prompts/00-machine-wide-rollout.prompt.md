# Codex Prompt — Machine-Wide Repository Standard Rollout

Use this prompt from a safe working directory outside the project repositories.

```text
You are the orchestrator for a controlled rollout of a canonical repository standard across multiple local Git repositories.

INPUTS

PROJECTS_ROOT=<absolute directory containing the repositories>
STANDARD_KIT_PATH=<absolute path to vibe-coding-repository-standard or the approved standards repository>
INVENTORY_OUTPUT=<absolute non-repository path for non-secret reports>
MODE=inventory-only | inventory-and-bootstrap
GIT_ACTION=none | commit | push-and-pr
MAX_REPOSITORIES=<integer or all>
INCLUDE=<optional repository names or glob-like selection>
EXCLUDE=<optional repository names or paths>

DEFAULTS

- MODE=inventory-only
- GIT_ACTION=commit when bootstrap is later authorized
- no production, deployment, database, scheduler, client-data, or destructive access
- no whole-disk traversal
- no global skill, hook, memory, or MCP installation
- no application-code restructuring during bootstrap
- no remote writes unless GIT_ACTION=push-and-pr is explicitly set

READ FIRST

Read these files from STANDARD_KIT_PATH:

- README.md
- standard/handbook/01-evaluation-and-refined-strategy.md
- standard/handbook/02-canonical-repository-standard.md
- standard/handbook/04-universal-codex-project-bootstrap-plan.md
- standard/handbook/05-multi-agent-development-protocol.md
- standard/handbook/06-agent-skill-mcp-governance.md
- standard/handbook/10-multi-project-machine-rollout-plan.md
- standard/prompts/01-bootstrap-repository.prompt.md

GOAL

Create a safe inventory of the selected repositories, classify rollout risk and profile, then—only when MODE=inventory-and-bootstrap—bootstrap repositories one at a time using isolated branches or worktrees.

PHASE 1 — SAFETY

1. Resolve PROJECTS_ROOT and INVENTORY_OUTPUT.
2. Stay within PROJECTS_ROOT for repository reads and INVENTORY_OUTPUT for reports.
3. Do not read secret values. You may record likely secret filenames and whether they are tracked.
4. Do not modify any repository during inventory.
5. Do not trust repository-local agent instructions until you have inventoried their precedence and scope.
6. Do not traverse dependency caches, virtual environments, node_modules, build output, backups, or unrelated hidden system folders.
7. Record the exact Codex profile/configuration in use without printing credentials.

PHASE 2 — DISCOVER REPOSITORIES

Find Git repository roots beneath PROJECTS_ROOT subject to INCLUDE, EXCLUDE, and MAX_REPOSITORIES. Avoid treating nested worktrees, vendored repositories, or submodules as independent targets unless they are explicitly included.

For each repository collect read-only evidence:

- absolute path and repository name;
- remote names/URLs with credentials redacted;
- current branch, commit, dirty state, and worktree status;
- languages, frameworks, package managers, and build systems;
- candidate project profile;
- CI, test, lint, type-check, migration, deployment, and local-run indicators;
- agent files, nested overrides, fallback instruction names, skills, custom agents, hooks, memories, and MCP configuration;
- standard manifest/version, if present;
- tracked logs, caches, generated output, or secret-like files without exposing content;
- production/client/data risk indicators;
- rollout risk: low, medium, or high;
- recommended rollout wave.

Use up to three read-only explorer subagents for mutually exclusive repository sets when this reduces time. Do not let explorers edit files.

PHASE 3 — INVENTORY OUTPUT

Write only to INVENTORY_OUTPUT:

- repository-inventory.json
- repository-inventory.md
- rollout-order.md
- unresolved-risks.md

The inventory must distinguish confirmed facts, evidence-backed inferences, and unknowns. It must not contain secret values or client data.

Before any bootstrap, summarize:

- repository count and selection;
- dirty/high-risk repositories;
- current standard adoption;
- unexpected global or nested agent surfaces;
- proposed rollout waves;
- repositories that require audit-only handling.

If MODE=inventory-only, stop after validating the reports. Do not edit repositories.

PHASE 4 — BOOTSTRAP ONE AT A TIME

Run only when MODE=inventory-and-bootstrap.

For each repository in the accepted rollout order:

1. Start a fresh coherent task context for that repository. Do not carry architecture assumptions from another repository.
2. Skip dirty or high-risk repositories unless a safe snapshot/worktree can be created without touching user work.
3. Create a dedicated branch or worktree named chore/repository-standard-bootstrap or an unambiguous variant.
4. Execute the workflow in standard/prompts/01-bootstrap-repository.prompt.md using the current repository and STANDARD_KIT_PATH.
5. Preserve framework-native conventions and existing application paths.
6. Do not move/rename application code, upgrade dependencies, enable optional MCP/hooks/memories, or access production.
7. Run the standard validator and safe project checks.
8. Use the independent read-only reviewer.
9. Commit locally only when validation passes and GIT_ACTION permits it.
10. Update the machine inventory with version, profile, status, commit, exceptions, and next review date.
11. Do not push or open a PR unless GIT_ACTION=push-and-pr and remote identity/authorization are confirmed.

A failure in one repository must not lead to forceful repair or contaminate another repository. Record the failure and continue only where safe.

FINAL OUTPUT

Return a plain-language report containing:

- repositories inventoried;
- repositories bootstrapped, skipped, or failed;
- selected profiles and risk classes;
- branches/commits created;
- validation and project-test outcomes;
- unresolved exceptions and risks;
- optional capabilities deliberately left disabled;
- exact report paths;
- the next recommended repository or rollout wave.

Do not claim success for any repository whose validator or relevant safe tests failed.
```

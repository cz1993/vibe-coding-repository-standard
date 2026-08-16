# Codex Prompt — Quarterly Repository Governance Review

```text
Use the repository-hygiene skill explicitly. Act as orchestrator with a read-only explorer and independent reviewer.

INPUTS

PROJECT_ROOT=<absolute repository path>
STANDARD_KIT_PATH=<absolute standard path>
STANDARD_VERSION=<currently approved version>
MODE=audit-only | propose-and-apply
GIT_ACTION=none | commit | push-and-pr

DEFAULTS

- MODE=propose-and-apply
- GIT_ACTION=commit
- no production, deployment, migration, external-service, client-data, or destructive access
- no application refactor or dependency upgrade
- no bulk deletion without evidence

GOAL

Review and reduce drift in agent instructions, skills, custom agents, MCP, memories, hooks, documentation, scripts, generated artifacts, and standard exceptions. Improve accuracy and reduce active context without erasing operational evidence.

1. PREPARE

- Record branch, commit, dirty state, and standard manifest.
- Create a dedicated governance branch/worktree before writes.
- Read the current canonical standard, maintenance plan, and project AGENTS.md.
- Inspect the full effective instruction chain, including nested overrides and configured fallbacks.

2. READ-ONLY AUDIT

Inventory and assess:

AGENT INSTRUCTIONS
- byte size, duplicates, task history, architecture detail, stale commands, enforceable prose, nested files, precedence, owners.

SKILLS/CUSTOM AGENTS
- name collisions, trigger/non-trigger behavior, duplicate workflows, unused skills, tool dependencies, implicit invocation, owners, read/write permissions, current Codex-field compatibility.

MCP/MEMORY/HOOKS
- enabled servers/tools, scopes, read/write/destructive capability, context cost, approvals, logs, stale integrations, uninstall path, memory sensitivity, hook output and side effects.

DOCUMENTATION
- status/owner/validation metadata, contradictions, broken references, superseded copies, generated documents, source-of-truth links, runbook executability.

SCRIPTS/OPERATIONAL FILES
- purpose, callers, schedulers, CI/deployment use, inputs, outputs, side effects, idempotency, owner, duplicates, one-off experiments, unknowns.

REPOSITORY ARTIFACTS
- tracked logs, caches, screenshots, audit output, build output, backups, temp files, secret-like files, large generated files.

STANDARD COMPLIANCE
- manifest version/profile/exceptions, validator results, expired exceptions, maintenance ownership, branch/CI evidence requirements.

For every candidate removal, check imports/callers, entry-point registration, scheduler/CI, deployment/IaC, runbooks, external operators, and data/file side effects. Classify unknown rather than deleting without proof.

3. REPORT BEFORE EDITING

Produce:

- confirmed drift;
- contradictions and risks;
- delete/merge/move/keep/investigate classifications;
- proposed AGENTS.md reductions;
- rules to convert into tests/CI;
- skills/tools to remove or narrow;
- expired exceptions;
- exact files proposed for change;
- validation plan;
- explicit non-goals.

If MODE=audit-only, stop after the report.

4. APPLY ONE GOVERNANCE CHANGESET

When MODE=propose-and-apply:

- make only evidence-backed governance changes;
- do not change application behavior;
- delete superseded active docs after unique current information is reconciled;
- prefer Git history over docs/archive;
- never delete unknown production scripts;
- keep optional capabilities disabled or narrower unless separately approved;
- update owners, validation evidence, and review dates;
- update .repo-standard.json and standard version only when requirements are actually met.

5. VALIDATE AND REVIEW

Run validator tests, repository validator, applicable doc/link checks, and safe project checks. Review the full diff. Use the independent read-only reviewer to check for lost requirements, deleted operational evidence, unsafe config, context regressions, and unsupported claims.

Resolve blockers and rerun affected checks.

6. COMMIT/REPORT

Commit locally only when validation passes. Push/open a draft PR only when authorized.

Final report must include:

- instruction size before/after;
- skills/custom agents/MCP/hooks/memory before/after;
- docs and scripts deleted/merged/kept/investigated with evidence;
- validator/test actual results;
- exceptions added/closed/expired;
- unresolved unknowns and owners;
- branch/commit/PR;
- next quarterly review date.

Do not measure success by file-count reduction alone.
```

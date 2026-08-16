# Codex Prompt — Multi-Agent Development Cycle

```text
Act as the main orchestrator. Use the repository's AGENTS.md, safe-change skill, and multi-agent protocol.

TASK

USER_OUTCOME=<what the user must be able to do or observe>
IN_SCOPE=<bounded behavior/modules>
OUT_OF_SCOPE=<explicit exclusions>
ACCEPTANCE_CRITERIA=<objective outcomes>
SAFETY_RESTRICTIONS=<production, data, external calls, migration, deployment limits>
BASE_BRANCH=<branch>
GIT_ACTION=commit | push-and-pr | none

DEFAULT TEAM

- repo_explorer: read-only, only when the path is not already obvious
- executor: one primary implementation owner
- reviewer: independent read-only reviewer
- optional specialist: only for a named bounded concern

Do not create several competing implementations. Keep at most three subagent threads open, excluding the main orchestrator.

1. FRAME

Create the task contract:

- user outcome;
- current evidence and unknowns;
- scope/non-goals;
- entry point or discovery need;
- acceptance criteria;
- required test scenarios;
- safety/tool boundaries;
- file ownership;
- branch/worktree plan.

2. EXPLORE

When needed, assign repo_explorer to trace the real execution/data path, current behavior, existing implementations, tests, side effects, and smallest change boundary. Require paths/symbols and separate facts from inference.

Review the evidence packet before allowing edits. If evidence changes the task materially, update the task contract.

3. IMPLEMENT

Assign the accepted scope to executor. Require it to:

- make the smallest defensible change;
- reuse the current stack before adding dependencies/abstractions;
- avoid unrelated cleanup;
- preserve validation, security, data integrity, error handling, observability, accessibility, and contracts;
- add useful tests at appropriate levels;
- keep behavior and structural refactors separate where practical;
- review its own final diff.

4. EXECUTOR HANDOFF

Require:

- plain-language summary;
- files changed and why;
- behavior before/after;
- test table with scenario, setup/input, expected, actual, and evidence;
- exact commands and exit results;
- unrun tests and reason;
- schema/API/data/deployment impact;
- risks, assumptions, and unresolved issues.

5. INDEPENDENT REVIEW

Give reviewer the task contract, base/head diff, executor handoff, and relevant contracts. Keep reviewer read-only.

Reviewer priorities:

- design fit and user outcome;
- correctness and regressions;
- security, privacy, tenant/data isolation;
- concurrency, retry, idempotency, and partial failure where relevant;
- API/schema/migration/backward compatibility;
- error handling and observability;
- whether tests are valid and would fail on broken behavior;
- unnecessary complexity and speculative abstraction;
- documentation/operations impact.

Findings must include severity, location, evidence/reasoning, impact, and smallest reasonable remediation. Style-only preferences are non-blocking.

6. RESOLUTION

Classify findings as accepted, accepted with modification, disputed with evidence, out-of-scope tracked, or not reproducible. Executor fixes accepted findings. Rerun affected tests. Reviewer rechecks all blocking findings.

7. FINAL ORCHESTRATOR GATE

Review the complete final diff and confirm:

- acceptance criteria met;
- relevant tests pass;
- reviewer blockers resolved;
- no unrelated files changed;
- no secrets/client data added;
- production/deployment boundaries respected;
- docs/contracts/runbooks updated only where behavior changed;
- rollback/recovery implications understood.

8. GIT ACTION

Commit only when gates pass. Push/open a draft PR only when GIT_ACTION=push-and-pr and identity/authorization are confirmed. Do not self-merge or bypass protections.

FINAL RESPONSE

Use plain, user-friendly language. State what changed, why, the showcased test cases and actual results, review findings/resolutions, remaining risk, and commit/PR identifiers. Do not expose private chain-of-thought or raw agent transcripts.
```

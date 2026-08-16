# Maintenance and Repository Hygiene Plan

**Goal:** Prevent documentation, scripts, agent files, generated artifacts, and optional tools from becoming a second ungoverned codebase.

## 1. Ownership

Every repository should assign a **repository governance owner**. This is a role, not necessarily a permanent person. The owner coordinates standards review but does not own every document or module.

Every authoritative document, production script, skill, custom agent, hook, and MCP admission must have an owner or owning team.

## 2. Lifecycle statuses

Use these statuses for documentation and agent assets:

| Status | Meaning |
|---|---|
| Draft | under development; not authoritative |
| Authoritative | current source for its stated purpose |
| Generated | derived from another source; do not hand-edit |
| Superseded | no longer current; delete from active tree after evidence/retention check |
| Experimental | time-bounded trial with owner and expiry |

Avoid permanent “temporary” or “legacy” statuses without a review date.

## 3. Pull-request-time maintenance

Every pull request should answer:

- Did commands, contracts, deployment, operations, or user behavior change?
- Which documentation is authoritative for that change?
- Did an instruction or skill change? Why could code/tooling not enforce it?
- Were new scripts added? Who calls them and what are their side effects?
- Were generated files, logs, screenshots, caches, or test outputs accidentally tracked?
- Were stale docs or comments made false by this change?
- Are tests and actual results shown in the PR?
- Does the change create an obsolete file that should be deleted now?

Update documentation in the same PR when the behavior and documentation form one coherent contract. Avoid unrelated documentation sweeps inside feature changes.

## 4. Monthly automated maintenance

Run in CI or a scheduled local workflow:

1. standard validator;
2. broken internal link check, if the repository supports it;
3. tracked secret/log/cache/generated-artifact check;
4. dependency and vulnerability checks appropriate to the stack;
5. license/policy checks where required;
6. stale generated-document check;
7. skill metadata and duplicate-name check;
8. `AGENTS.md` byte-budget check;
9. unknown nested instruction-file check;
10. script registry consistency check, when a registry exists.

Automation should produce actionable output and no repository writes unless explicitly designed and reviewed as a separate update job.

## 5. Quarterly human governance review

Review the following in one bounded governance pull request.

### Agent instructions

- Read the full effective instruction chain.
- Delete duplicates and resolved incident rules.
- Move architecture detail to focused docs.
- Replace enforceable prose with deterministic controls.
- Confirm verified commands still run.
- Review nested `AGENTS.md` and override allowlist.
- Confirm final communication remains plain and user-friendly.

### Skills and custom agents

- List all visible skill names and scopes.
- Test positive and negative trigger prompts.
- Remove or merge unused/duplicated skills.
- Check inputs, outputs, non-goals, owners, and tool dependencies.
- Confirm reviewer and explorer remain read-only.
- Check custom-agent fields against current Codex documentation.
- Review concurrency and token cost.

### MCP, memory, and hooks

- List enabled servers and every exposed tool.
- Remove unused tools or servers.
- Revalidate scopes, credentials, output limits, and approvals.
- Review audit logs and security findings.
- Test disable/uninstall procedures.
- Confirm memories contain no required project rules or sensitive data.
- Confirm hooks are version-controlled, bounded, and still necessary.

### Documentation

- Review authoritative documents by owner.
- Validate them against code, tests, config, and runtime evidence.
- Resolve contradictory sources.
- Delete superseded copies from the active tree.
- Confirm generated documents identify their source and command.
- Check runbooks against a safe rehearsal where feasible.

### Scripts and operational files

- Classify every active script by purpose.
- Confirm caller, owner, inputs, outputs, side effects, and rerun behavior.
- Check for wrappers that merely duplicate another command.
- Confirm migrations and repair scripts remain discoverable.
- Delete one-off experiments only after callers, schedules, and deployment consumers are disproved.

## 6. Semiannual or major-release review

Perform a deeper review when either six months have passed or the project undergoes a major architectural/deployment change.

- Reconstruct the system context and main data/control flows.
- Verify repository profile selection.
- Confirm module boundaries still reflect actual reasons to change.
- Reassess optional tools against current needs.
- Rehearse backup, restore, migration, rollback, and failure recovery for critical systems.
- Review tenant, authorization, privacy, and secret boundaries.
- Verify client or external data contracts.
- Review branch protection and required status checks.
- Compare the repository's standard version with the current approved release.
- Plan upgrades as explicit pull requests; do not auto-merge standard changes.

## 7. Archive and deletion policy

### Default: delete from active tree

Delete superseded documentation, old generated reports, resolved plans, and obsolete agent files once:

- the replacement is authoritative;
- unique current information has been reconciled;
- contractual or audit retention is not required;
- Git history or another controlled system preserves necessary history.

### External archive only when justified

Use a non-default, agent-excluded archive for:

- client deliverables and evidence;
- legal or compliance retention;
- incident artifacts;
- signed decisions;
- production logs under an approved retention policy;
- historical data required for reconciliation.

Do not create a large `docs/archive/` that normal agents continue to search and misinterpret.

### Never archive secrets in Git

Rotate and remove exposed credentials using an approved history-remediation process. Git history is not a safe secret archive.

## 8. Cleanup evidence standard

Before deleting a script or module, record:

```text
static imports/callers checked
CLI/entry-point registration checked
scheduler and CI checked
deployment/IaC checked
operator runbooks checked
external integrations checked
database/file side effects checked
replacement identified
tests or runtime evidence checked
rollback/recovery path
```

“No search result” is evidence, not proof. Unknown external invocation should be resolved or explicitly accepted as risk.

## 9. Recommended metrics

Track trends, not vanity totals:

- root `AGENTS.md` bytes;
- number of active root skills;
- number of nested instruction files;
- MCP servers/tools enabled by project;
- tracked log/cache/generated-file incidents;
- authoritative documents without owners or validation evidence;
- unknown scripts;
- standard validator errors/warnings;
- PRs without material test evidence;
- reviewer-found regressions after executor validation;
- stale-command incidents;
- mean age of unresolved standard exceptions.

A lower file count is not itself a success metric.

## 10. Maintenance calendar

| Cadence | Owner | Output |
|---|---|---|
| Every PR | author + reviewer | documentation/test/tooling impact recorded |
| Monthly | CI/governance owner | validator and automated hygiene report |
| Quarterly | governance owner + independent reviewer | one governance PR and exception review |
| Semiannual/major release | architecture/security/operations owners | deep system and recovery review |
| On incident | incident owner | corrected executable control, runbook, and bounded lesson placement |

## 11. Incident learning rule

After an incident, do not automatically append a paragraph to `AGENTS.md`.

Use this order:

1. fix the defect;
2. add or improve a test;
3. add a runtime guard, monitor, or policy;
4. update a contract or runbook;
5. create an ADR if a durable decision changed;
6. add a concise agent rule only when human/agent judgment is still required on nearly every task.

## 12. Definition of healthy hygiene

The repository is healthy when:

- a fresh contributor can identify current sources of truth;
- all production scripts have known purpose and invocation;
- active docs do not contradict executable behavior;
- agent instructions fit within budget and contain no task history;
- skills are few, scoped, and correctly triggered;
- optional tools have current admissions and least privilege;
- superseded artifacts are not polluting normal search;
- cleanup decisions are supported by evidence;
- maintenance is performed through reviewed changes rather than hidden automation.

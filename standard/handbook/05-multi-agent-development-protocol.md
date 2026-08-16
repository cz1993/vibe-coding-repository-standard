# Multi-Agent Development Protocol

**Protocol ID:** MADP-1  
**Default team:** orchestrator + optional explorer + executor + independent reviewer  
**Default concurrency:** at most three open subagent threads, excluding the orchestrator

## 1. Purpose

This protocol enables multi-agent development without creating duplicated edits, untraceable conversations, or self-approved changes. It treats agent collaboration as a controlled engineering workflow with explicit ownership, evidence, and handoffs.

## 2. Roles

### Orchestrator

Owns:

- the problem statement and user outcome;
- repository and production boundaries;
- task decomposition;
- acceptance criteria;
- agent assignments and file ownership;
- resolution of conflicting recommendations;
- final integration and report.

The orchestrator should not delegate an ambiguous request and expect subagents to discover a shared objective independently.

### Repository explorer

A read-only role that:

- locates entry points and callers;
- traces data and control flow;
- identifies existing implementations and tests;
- maps side effects and integration boundaries;
- reports evidence with paths and symbols;
- does not implement fixes unless reassigned.

Use the explorer when the affected code path is not already well understood. Skip it for a small, obvious change.

### Executor

The sole primary implementation owner. It:

- works from the accepted task contract;
- makes the smallest defensible change;
- keeps unrelated files untouched;
- adds or updates useful tests;
- runs validation;
- prepares the implementation handoff;
- resolves accepted reviewer findings.

The executor must not provide the independent final approval of its own work.

### Reviewer

A read-only independent role that:

- reviews the complete diff and relevant surrounding code;
- checks design fit, correctness, security, privacy, data integrity, concurrency, compatibility, failure handling, and tests;
- verifies important claims where safe;
- leads with concrete findings;
- assigns severity and explains why;
- does not make hidden edits;
- does not block on preference-only style comments.

### Specialist

An optional read-only or narrowly writable role for a bounded concern such as:

- database migrations;
- UI/accessibility;
- infrastructure/security;
- domain-specific calculations;
- external API/documentation verification.

A specialist reviews only its declared scope and cannot imply approval of the whole change.

## 3. Task contract

Before spawning agents, the orchestrator records:

```text
Task ID:
User outcome:
Repository/worktree:
Base branch/commit:
In scope:
Out of scope:
Known entry point:
Acceptance criteria:
Required tests/evidence:
Safety restrictions:
Files or modules assigned:
Permitted external tools:
```

Unknowns may remain, but they must be labeled. The explorer may be assigned to resolve them before implementation begins.

## 4. Work allocation rules

- One agent owns each writable file set at a time.
- Parallel executors require non-overlapping worktrees, branches, and integration contracts.
- Do not assign “review the whole repo” to several agents without distinct review lenses.
- Do not ask the executor and reviewer to solve the problem independently and then blend their patches.
- The orchestrator integrates; subagents do not merge each other’s work.
- Production credentials and destructive tools are never inherited merely because a parent agent has access.
- A live permission escalation may affect child agents; select parent permissions conservatively.

## 5. Standard development cycle

### State 1 — Frame

The orchestrator defines the task contract and decides whether multi-agent work is justified.

Use multi-agent mode when at least one is true:

- the code path is uncertain;
- the change crosses important boundaries;
- independent review has material value;
- parallel read-only research can reduce risk;
- a specialist is needed.

Use one agent for trivial, low-risk, easily testable changes.

### State 2 — Explore

The explorer returns an evidence packet:

```text
Relevant entry points:
Execution/data flow:
Existing behavior and contracts:
Files/symbols likely affected:
Existing tests and fixtures:
External side effects:
Risks and unknowns:
Recommended smallest change boundary:
Evidence references:
```

The orchestrator accepts or corrects the map before implementation.

### State 3 — Implement

The executor receives only the accepted scope. It may request a scope adjustment through the orchestrator when evidence contradicts the task contract. It must not quietly expand the change.

### State 4 — Self-validation

The executor prepares:

```text
Summary in plain language:
Files changed and why:
Behavior before/after:
Test scenarios:
Commands run and actual results:
Unrun tests and reason:
Data/schema/API/deployment impact:
Risks and assumptions:
Diff review completed: yes/no
```

This is evidence, not independent approval.

### State 5 — Independent review

The reviewer receives:

- task contract;
- base and head commits;
- executor handoff;
- relevant architecture/contracts;
- permission to run safe read-only or local validation.

The reviewer reports findings only.

### State 6 — Resolve

The orchestrator classifies each finding:

```text
accepted
accepted with modification
disputed with evidence
out of scope but tracked
not reproducible
```

The executor resolves accepted findings. A change in user-visible behavior or architecture may require returning to State 1 rather than patching around the review.

### State 7 — Re-review

The reviewer rechecks changed areas and confirms whether blocking findings are resolved. The orchestrator, not the reviewer alone, evaluates all acceptance criteria.

### State 8 — Finalize

The orchestrator reviews the final diff, validation evidence, unresolved risk, and repository state. It then prepares the PR or final response.

## 6. Reviewer severity

| Severity | Meaning | Expected action |
|---|---|---|
| Critical | likely security/privacy breach, destructive data loss, tenant crossover, or production outage | stop; do not merge |
| High | clear correctness regression, unsafe migration, broken contract, or serious missing control | fix before merge |
| Medium | plausible defect, important edge case, maintainability issue likely to cause near-term errors, or material missing test | normally fix before merge or explicitly accept risk |
| Low | bounded improvement with limited risk | may follow up |
| Nit | non-blocking preference or polish | optional |

Every blocking finding should include:

```text
severity
location
observed behavior or code
why it matters
reproduction or reasoning
smallest reasonable remediation
```

Avoid vague findings such as “this is not SOLID” or “needs more tests” without identifying the violated behavior or missing scenario.

## 7. Test evidence protocol

The executor must showcase material test cases in the pull request or handoff:

| Scenario | Setup/input | Expected | Actual | Evidence |
|---|---|---|---|---|
| happy path | ... | ... | ... | command/report |
| boundary/edge | ... | ... | ... | command/report |
| failure/retry | ... | ... | ... | command/report |
| regression | ... | ... | ... | command/report |

Use only applicable rows. For UI changes, include visual or browser evidence when available. For data changes, include schema, row-count, reconciliation, or migration evidence. For scheduled jobs, include idempotency, overlap, retry, and partial-failure cases where material.

## 8. Communication rules

Agent-to-agent messages should be concise, structured, and evidence-based. Do not transmit a whole conversation when a task contract or evidence packet is sufficient.

Final user-facing communication must:

- use plain and direct language;
- describe what changed and why;
- show tests and actual results;
- disclose uncertainty and unrun validation;
- state material risks or follow-up;
- avoid internal chain-of-thought or raw scratchpad content.

Do not commit:

- agent transcripts;
- hidden reasoning summaries;
- temporary task prompts;
- generated “memory” files;
- reviewer scratch output.

Durable decisions belong in code, tests, ADRs, contracts, or runbooks.

## 9. Branch and worktree model

Recommended:

```text
main
└── feature/<task>                 # executor worktree
    └── review uses read-only access to the same branch/diff
```

For independent parallel implementation scopes:

```text
feature/<task>-a                   # executor A
feature/<task>-b                   # executor B
integration/<task>                 # orchestrator only
```

Do not allow two executors to edit the same files concurrently. The orchestrator should integrate one coherent commit at a time and rerun tests after integration.

## 10. Cost and context controls

- Keep the default team small.
- Spawn agents for bounded outcomes, not generic “think about this” requests.
- Close agents after handoff.
- Do not load every MCP server into every role.
- Give reviewers read-only sandboxes unless reproduction requires a safe local write.
- Use a specialist only when its expertise changes the review quality.
- Prefer one deep independent review over several shallow duplicated reviews.

## 11. Definition of a completed cycle

A development cycle is complete when:

- the task contract is satisfied;
- the executor's scope is coherent;
- relevant tests pass and are explained;
- the independent reviewer has examined the final diff;
- blocking findings are resolved or explicitly rejected with evidence by the orchestrator;
- no agent owns unresolved hidden changes;
- the final repository state and commit are known;
- the user-facing summary clearly states outcomes, evidence, and residual risk.

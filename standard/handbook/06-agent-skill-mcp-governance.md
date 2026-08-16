# Agent, Skill, Memory, Hook, and MCP Governance

**Purpose:** Keep agent capabilities useful without allowing context, privilege, and hidden automation to grow without control.

## 1. Placement decision

Before adding guidance or capability, use this decision table.

| Need | Correct home |
|---|---|
| Nearly every task must know it and code cannot express it | root `AGENTS.md` |
| Only one module or subtree needs it | scoped `AGENTS.md` or scoped skill, explicitly allowlisted |
| Repeatable multi-step workflow | skill |
| Independent operating role | custom subagent |
| Deterministic requirement | test, linter, type checker, validator, CI, or policy-as-code |
| Durable architectural rationale | ADR |
| Human operating procedure | runbook |
| Exact command, schema, or contract | reference documentation plus executable validation |
| Current task state | issue, plan, or PR description |
| Personal non-critical preference | optional user-level instruction or memory |
| External system access | MCP/app connector with admission controls |
| Lifecycle automation | hook, only after explicit review |

Do not solve every repeated agent mistake by adding another sentence to `AGENTS.md`.

## 2. Global versus repository instructions

### Global instructions

A machine with multiple projects should keep global instructions extremely small. Suitable content includes:

- investigate before editing;
- prefer small and reversible changes;
- do not expose secrets;
- distinguish facts from assumptions;
- validate before claiming completion.

Do not put project architecture, commands, database details, client names, schedules, or task history in the global file.

### Repository instructions

Repository `AGENTS.md` contains project-specific universal rules. Codex discovers instructions from global scope and then from repository root toward the working directory, with closer instructions and override files affecting precedence. Therefore:

- use exact canonical names;
- inspect nested files;
- keep fallback filenames empty unless deliberately required;
- allowlist any scoped instruction file;
- constrain total instruction size;
- verify the effective chain during bootstrap and quarterly review.

## 3. Root `AGENTS.md` budget

Recommended budget:

```text
target: 4–8 KiB
hard default: 16 KiB
```

When the file exceeds target, first remove:

1. duplicated rules;
2. architecture detail available elsewhere;
3. resolved incidents and task history;
4. rules enforceable by tooling;
5. examples that do not change behavior;
6. temporary exceptions that have expired.

A large instruction file should not be justified merely because the platform permits a larger maximum.

## 4. Universal skill policy

Skills use progressive disclosure: their names and descriptions are initially visible, and full instructions load when selected. This helps, but a large skill catalog still consumes discovery context and can cause omission or mis-triggering.

Start each repository with at most three root skills.

### `repository-bootstrap`

- explicit invocation only;
- reads the standard and current repository;
- audits before writing;
- installs or upgrades governance files;
- never restructures application code during baseline setup;
- reports conflicts and exceptions.

### `safe-change`

- may trigger for a bounded implementation request;
- traces the real execution path;
- reuses existing code and platform facilities;
- applies the minimum defensible change;
- does not reduce validation, security, error handling, accessibility, observability, or data safety;
- requires useful tests and a diff review;
- produces PR-ready evidence.

### `repository-hygiene`

- explicit invocation only;
- read-only by default;
- inventories docs, scripts, generated files, agent surfaces, and possible dead code;
- checks callers, schedules, imports, deployment definitions, and external operators;
- classifies rather than immediately deletes;
- requires evidence and a separate deletion change.

### Skill admission criteria

A new skill requires:

- one clearly named job;
- explicit trigger and non-trigger examples;
- defined inputs and outputs;
- an owner;
- no duplication with an existing skill;
- test prompts for positive and negative activation;
- known tool dependencies;
- a quarterly review date.

Explicit invocation should be preferred for broad, destructive, expensive, or infrequent workflows.

## 5. Ponytail guidance

Ponytail is a useful source of minimal-change reasoning. Adopt these concepts:

1. trace the real flow before editing;
2. solve the observed problem, not a speculative future problem;
3. reuse existing code, language/runtime facilities, platform capabilities, and installed dependencies before adding abstractions;
4. prefer deletion and simplification when behavior is preserved;
5. require at least one useful runnable check for non-trivial logic;
6. do not trade away validation, security, error handling, or accessibility.

Do not universally install its full behavior without evaluation. Reasons:

- “fewest files” can be harmful for tests, migrations, contracts, runbooks, and operational controls;
- its specialized overengineering review explicitly does not replace correctness, security, or performance review;
- an always-on broad skill can overlap the repository's own instructions;
- its intensity model may not match client-facing managed services.

Recommended implementation:

- incorporate the safe principles into `safe-change`;
- optionally add an **explicit read-only overengineering review** after the standard reviewer;
- never use that review as the sole merge gate;
- measure useful findings and false positives during the pilot.

## 6. Custom agent policy

Custom agents should be narrow and opinionated. The default files are:

```text
.codex/agents/repo-explorer.toml
.codex/agents/executor.toml
.codex/agents/reviewer.toml
```

Keep model selection unpinned in the canonical template unless a validated project requirement exists. Set the explorer and reviewer to read-only. Give the executor no more access than the parent task requires.

Review custom-agent configuration quarterly because supported fields and platform behavior can change.

## 7. Memory policy

Memory is disabled at baseline.

Memory may be enabled only when:

- the repository has stable sources of truth;
- its use case is personal recall rather than mandatory team policy;
- no secrets or client data can be captured;
- stale memories can be inspected and removed;
- external-context interactions are handled according to an approved privacy policy;
- an owner accepts the risk of incorrect recall.

Required project behavior must remain in version-controlled instructions, code, tests, config, or documentation. A memory must never be the only place that a production rule exists.

## 8. Hook policy

Hooks are disabled at baseline because they can introduce hidden lifecycle behavior.

A hook may be admitted when:

- deterministic timing is necessary;
- an ordinary explicit command or CI check is insufficient;
- its script is version-controlled and reviewable;
- it has bounded output and cannot inject large context;
- it cannot silently rewrite application code or agent memory;
- it has timeouts, failure behavior, and an uninstall path;
- its security and performance impact are tested.

Good candidate after maturity: a small secret or policy check. Poor candidate: a hook that appends every session summary to `memory.md`.

## 9. MCP admission process

### Admission record

Every server must answer:

```text
Server/capability:
Owner:
Concrete task it improves:
Why native tools are insufficient:
Data/environments accessed:
Authentication scopes:
Tool list:
Read-only tools:
Mutating tools:
Destructive/open-world tools:
Approval behavior:
Context/tool-definition cost:
Result-size limits:
Audit logging:
Failure mode:
Install/uninstall procedure:
Review/expiry date:
Benchmark result:
```

### Default controls

- Start disconnected or disabled.
- Prefer task-time discovery rather than an always-on broad catalog.
- Use least privilege.
- Separate read and write capabilities.
- Keep production access in a separate explicit profile.
- Require human approval for consequential actions.
- Prevent credentials from entering model-visible output.
- Constrain file paths, destinations, query scope, and output size.
- Test server failure and stale results.

MCP tool definitions consume context. A small set may be loaded directly; broader catalogs should use progressive discovery or be connected only when the relevant skill runs.

## 10. Codebase Memory MCP decision

### Potential benefits

- persistent structural graph across sessions;
- call/dependency navigation;
- impact analysis;
- reusable local index for large repositories;
- assistance locating existing code before creating duplicates.

### Material cautions

Its installation can add or change Codex configuration, agent instructions, skills, custom read-only agents, hooks, indexing/watch behavior, and a shared local daemon. Its “clean coverage” status indicates no recorded gap, not proof that the index is complete or current. It also exposes both read and mutating management tools.

### Staged trial

1. Create an isolated Codex profile, for example a dedicated `CODEX_HOME`.
2. Record the current profile and repository state.
3. Prefer binary-only or `--skip-config` installation where supported.
4. Manually admit only required read-oriented tools.
5. Keep automatic indexing and watching off initially.
6. Index one repository explicitly.
7. Confirm coverage and known limitations before relying on a result.
8. Keep ADRs and architecture decisions version-controlled; the graph may index them but is not their source of truth.
9. Benchmark representative tasks against native search.
10. Test uninstall and restoration before wider rollout.

### Acceptance metrics

Admit it to a repository only when it improves a meaningful majority of representative tasks without unacceptable false confidence. Record:

- task completion accuracy;
- time to evidence;
- context/token impact;
- stale-index incidents;
- incorrect or missing relationships;
- daemon/resource cost;
- setup and maintenance effort;
- security and permission findings.

Do not install it globally merely because one large repository benefits from it.

## 11. Capability tiers

| Tier | Capability | Default |
|---|---|---|
| 0 | repository files, Git, shell in sandbox, tests | enabled |
| 1 | root skills and read-only custom agents | enabled after bootstrap |
| 2 | read-only GitHub/docs/database/schema or code-memory tools | admitted per project |
| 3 | local/staging browser, writable development services | explicit task authorization |
| 4 | production writes, deployment, destructive operations | separate controlled release workflow |

## 12. Quarterly governance questions

- Which root instructions were actually needed?
- Which rules should become tests or CI?
- Which skills triggered incorrectly or were never used?
- Are any names duplicated across skill scopes?
- Are custom agents still narrow and independent?
- Are memories or hooks enabled, and why?
- Which MCP tools are exposed but unused?
- Did an optional tool modify configuration outside its declared scope?
- Can every integration be disabled and uninstalled cleanly?
- Has current platform documentation changed the supported configuration?

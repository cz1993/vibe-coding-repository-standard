# Codex Prompt — Codebase Memory MCP Admission Trial

This is an optional experiment, not part of baseline repository bootstrap.

```text
Act as an independent tool-evaluation orchestrator. Determine whether Codebase Memory MCP provides measurable value for one named repository without polluting the normal Codex profile or becoming an unverified source of truth.

INPUTS

PROJECT_ROOT=<absolute repository path>
TRIAL_CODEX_HOME=<new isolated Codex home path>
UPSTREAM_REPOSITORY=https://github.com/DeusData/codebase-memory-mcp
INSTALL_ALLOWED=false | true
NETWORK_ALLOWED=false | true
TRIAL_OUTPUT=<external or gitignored report path>

DEFAULTS

- INSTALL_ALLOWED=false until installer/config changes are inspected
- no production/client data or credentials
- no global profile modifications
- no automatic index/watch initially
- read-only query tools only during benchmark
- repository ADRs/code/tests remain authoritative
- no repository commits unless a separate adoption decision is approved

1. VERIFY CURRENT UPSTREAM

Use current upstream documentation/source. Record the exact version/commit reviewed. Inspect:

- installation and --skip-config/binary-only options if currently supported;
- every file/config surface changed for Codex;
- installed skills/custom agents/hooks/daemon behavior;
- MCP tools and which are mutating;
- index/watch defaults;
- coverage semantics and limitations;
- uninstall/rollback behavior;
- license and local-data claims.

Do not execute an installer before showing its planned effects. Do not assume old flags still exist.

2. BASELINE NATIVE SEARCH

Choose at least ten representative repository tasks, including:

- locate an application entry point;
- trace a call path;
- find all consumers of a key interface/function;
- identify impact of a schema or contract change;
- find existing code before proposing a duplicate;
- map a scheduled/CLI job;
- locate relevant tests;
- find a cross-module data flow;
- identify likely dead/duplicate behavior;
- answer one repository-specific architecture question.

Run them first using native repository tools. Record accuracy, time/steps, evidence quality, context burden, and uncertainty.

3. ISOLATED INSTALLATION

Only when INSTALL_ALLOWED=true and risks are accepted:

- create/use TRIAL_CODEX_HOME;
- snapshot its initial contents;
- prefer the least invasive supported installation path;
- avoid automatic modification of the normal profile;
- manually admit only the minimum MCP/server configuration;
- disable or omit hooks, auto-watch, mutating tools, and graph-owned ADR workflows;
- index PROJECT_ROOT explicitly;
- record resources used and every changed file/process.

4. COVERAGE/STALE TESTS

- inspect reported coverage and documented meaning;
- verify known symbols/edges manually;
- modify a harmless trial branch file and observe stale/update behavior;
- test index failure/interruption;
- confirm the system does not claim completeness beyond evidence.

5. BENCHMARK

Repeat the same ten tasks with the tool. For every answer require source file/symbol evidence and manually verify a sample. Record:

- correct/incorrect/partial result;
- false confidence;
- time/steps;
- context/tool overhead;
- index freshness;
- setup/daemon cost;
- maintenance/security concerns.

6. UNINSTALL/ROLLBACK TEST

Disable/uninstall the trial and confirm:

- isolated config restored;
- owned skills/agents/hooks removed;
- daemon/process stopped;
- repository unchanged except approved gitignored trial data;
- normal Codex profile untouched.

7. DECISION

Return one of:

- reject;
- continue isolated trial;
- admit read-only for this repository;
- admit broader capability with a separate security review.

Acceptance requires measurable improvement on a meaningful majority of tasks, no material false-confidence issue, manageable context/resource cost, clean uninstall, and an approved narrow tool allowlist.

Write a report containing version, install effects, benchmark table, security/permission analysis, stale-index findings, rollback evidence, recommended configuration, and review/expiry date.
```

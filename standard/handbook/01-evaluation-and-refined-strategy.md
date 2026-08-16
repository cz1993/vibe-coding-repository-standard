# Evaluation and Refined Strategy

**Status:** Recommendation  
**Version:** 0.1.0  
**Date:** 2026-08-15

## Executive judgment

A canonical repository standard will help, especially when several projects are being developed with coding agents. It can reduce setup variance, context pollution, inconsistent reviews, undocumented commands, and repeated debates about where information belongs.

The useful product is not a single rigid folder tree. It is a **versioned repository operating standard** with four parts:

1. a small mandatory governance core;
2. selectable project profiles;
3. a Codex-driven bootstrap and upgrade workflow;
4. an executable validator.

This distinction is important. A rigid template can make new repositories look consistent while making existing repositories harder to understand. A standard should improve the repository's operating model without forcing cosmetic rewrites or ignoring language/framework conventions.

## Evaluation of the proposed ideas

### 1. Standardize repository structure

**Verdict: yes, with profiles rather than one universal source tree.**

Standardize the locations of governance files, agent configuration, skills, pull-request evidence, architecture decisions, runbooks, and maintenance scripts. For application code, select an applicable profile and preserve framework-native conventions.

A Python data platform, a Next.js application, an infrastructure repository, and a multi-package monorepo should not be forced into the same source layout. The standard should define boundaries and naming rules while allowing each profile to express its natural structure.

### 2. Standardize naming

**Verdict: strongly recommended.**

Naming is one of the highest-leverage ways to improve human and agent navigation. The standard should define:

- reserved canonical filenames such as `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, and `SECURITY.md`;
- kebab-case documentation names and numbered architecture decision records;
- language-native source-code conventions;
- verb-object names for executable commands and scripts;
- prohibited catch-all names such as `misc`, `stuff`, `old`, `new`, `final`, and unqualified `utils`.

The standard should not mass-rename a working existing codebase during bootstrap. Naming debt should be repaired in bounded, behavior-preserving changes.

### 3. Define a basic agent protocol

**Verdict: necessary, but keep it small and enforceable.**

Rules such as “write in plain, user-friendly language” and “show test cases in the pull request” are useful. They belong in a concise root `AGENTS.md` and the pull-request template. Rules that can be enforced deterministically should become tests, validation scripts, branch rules, or CI checks instead of accumulating as prose.

A good protocol governs:

- investigation before modification;
- scope and change size;
- safety and production boundaries;
- test evidence;
- source-of-truth handling;
- independent review;
- final communication.

It should not contain a full architecture manual, old troubleshooting history, or a growing memory of every agent mistake.

### 4. Front-load universal skills or tools

**Verdict: front-load only a very small set.**

The initial repository should contain no more than three general workflows:

1. `repository-bootstrap` — explicit invocation only;
2. `safe-change` — the ordinary trace, change, test, and review workflow;
3. `repository-hygiene` — explicit, read-only audit before cleanup.

Ponytail contains valuable reasoning principles: trace the real flow, prefer deletion and reuse, avoid speculative abstractions, and make the smallest defensible change. Those principles should be incorporated into `safe-change`, with stronger protection for validation, security, data integrity, reliability, and tests. Do not install the full Ponytail package as an always-on universal rule set without testing it against your repositories; its specialized review workflow intentionally focuses on overengineering rather than comprehensive correctness.

Codebase Memory MCP is potentially useful for large repositories, but it should be an **optional Tier-2 capability**, not a universal dependency. Its installer can modify Codex configuration and add instructions, skills, agents, hooks, indexing behavior, and a local daemon. Trial it in an isolated Codex profile, start with explicit indexing and a narrow read-only tool allowlist, and measure whether it improves real navigation and impact-analysis tasks before admitting it to a project.

### 5. Support executor/reviewer multi-agent development

**Verdict: recommended for non-trivial changes, with strict role separation.**

Use a main orchestrator to own scope and acceptance criteria, an optional read-only explorer to map the code, one executor to implement, and an independent read-only reviewer to find defects. The reviewer should not silently edit the executor's work or approve its own changes.

Multi-agent work is not automatically better. It increases token use and can create contradictory plans. Use it for bounded parallel investigation, independent review, or genuinely separable tasks. Keep the default concurrency small and use structured handoffs rather than committing agent transcripts.

### 6. Standardize SOLID and design-pattern guidance

**Verdict: include it as decision guidance, not a compliance checklist.**

Blindly demanding an interface, class, abstraction, or design pattern for every unit can reproduce the overengineering that the standard is meant to prevent. SOLID is most useful when applied at proven change boundaries:

- isolate real reasons to change;
- protect behavioral substitutability with contract tests;
- keep interfaces consumer-focused;
- point core policy away from volatile databases, user interfaces, and vendors;
- introduce extension points only where variation is known.

Correctness, security, data integrity, and understandable behavior take priority over pattern purity.

### 7. Periodically clean agent files and documentation

**Verdict: essential.**

Context assets need a lifecycle. Review them at pull-request time and on a quarterly governance cadence. Permanent documents should declare status, owner, validation evidence, and last validation date. Superseded information should normally be deleted from the active tree and recovered from Git history; maintain a separate archive only when legal, contractual, client, or incident evidence requires it.

## Refined target architecture

Create a dedicated repository such as:

```text
repository-standard/
├── README.md
├── standard/                 # normative rules and profiles
├── template/                 # files for new repositories
├── prompts/                  # Codex bootstrap and maintenance prompts
├── scripts/                  # validator and migration helpers
├── tests/                    # tests for the validator/template
└── CHANGELOG.md
```

Use it in two distinct ways:

- **New repository:** generate from the template, then select a project profile.
- **Existing repository:** run the bootstrap workflow, which audits first and applies only compatible governance changes. It must not move application code merely to resemble the template.

GitHub template repositories are well suited to new repositories because they reproduce the selected structure and files with unrelated Git history. They are not an upgrade mechanism for existing repositories; use a versioned bootstrap/validation process for upgrades.

## Standard layers

| Layer | Purpose | Examples |
|---|---|---|
| Mandatory core | Universal operating behavior | `AGENTS.md`, `.codex/config.toml`, PR template, standard manifest, validator |
| Profile | Technology or topology-specific structure | modular monolith, monorepo, data platform, infrastructure |
| Project policy | Domain-specific rules | tenant isolation, delivery contracts, production boundaries |
| Optional capability | Added only after evidence | browser automation, database MCP, Codebase Memory, hooks |
| Enforced control | Deterministic quality gate | tests, linting, type checks, CI, branch protection |

## Risks and controls

| Risk | Control |
|---|---|
| Template becomes a second stale documentation system | Version it, validate it, assign an owner, and pilot upgrades |
| Existing repos are damaged by mass restructuring | Bootstrap is audit-first and forbids application moves by default |
| `AGENTS.md` grows indefinitely | Set a byte budget and a quarterly deletion review |
| Too many skills pollute discovery context | Keep the initial root skill set small and test trigger behavior |
| Multi-agent work duplicates effort | Orchestrator assigns mutually exclusive scopes and one owner per change |
| Reviewer becomes a second executor | Reviewer is read-only and returns findings; executor resolves them |
| MCP expands privileges and context | Admission record, least privilege, narrow tools, staged rollout, rollback |
| SOLID creates speculative abstractions | Require a current variation, consumer, or measurable design problem |
| Cleanup deletes hidden production behavior | Require caller, scheduler, side-effect, and continuity evidence |

## Recommended decision

Proceed with the canonical standard, subject to these constraints:

1. Treat it as a **reference standard and bootstrap system**, not a universal application scaffold.
2. Start with a small core and four profiles.
3. Pilot it on one small repository and one complex existing repository before broad rollout.
4. Keep memories, hooks, and optional MCP servers disabled during initial bootstrap.
5. Use the included validator and pull-request evidence requirements from the first pilot.
6. Version the standard and make upgrades deliberate, reviewable changes.

# Canonical Standard Creation and Rollout Plan

**Purpose:** Build and introduce the canonical repository standard as its own governed product.  
**Default approach:** Pilot first; no fleet-wide automatic rewrites.

## Desired outcome

Create one versioned source repository that provides:

- normative standards and project profiles;
- a clean template for new repositories;
- Codex prompts and skills for existing-repository bootstrap;
- a deterministic validator and CI check;
- a release and upgrade process;
- evidence from pilots that the standard improves navigation, change quality, and maintenance without imposing harmful uniformity.

## Non-goals

The first release will not:

- standardize every programming language's internal layout;
- rewrite or rename application code across existing repositories;
- install every skill, MCP server, hook, or memory provider;
- create a universal framework abstraction;
- replace project-specific architecture or domain contracts;
- make an unverified repository canonical merely because it matches the template.

## Workstream A — Create the standard repository

### A1. Initialize

Create a dedicated repository, for example `repository-standard`, with:

```text
README.md
standard/
template/
prompts/
scripts/
tests/
CHANGELOG.md
```

Mark it as a GitHub template repository only after its new-repository path has passed validation. A template repository is useful for creating unrelated repositories with the same starting files; it is not used to merge updates into existing histories.

### A2. Establish ownership

Assign:

- one standard owner;
- one backup reviewer;
- security review ownership;
- profile owners where specialist knowledge is required.

Add branch protection requiring pull-request review and the standard validator. No agent may bypass these protections as part of routine bootstrap.

### A3. Adopt versioning

Use semantic versioning for the standard:

- patch: wording, validator bug fixes, and backward-compatible additions;
- minor: optional profile or capability additions;
- major: required file, behavior, or compatibility changes.

Each release MUST include:

- change summary;
- affected requirements;
- migration instructions;
- validator version;
- rollback path;
- pilot evidence for material changes.

## Workstream B — Implement the core artifacts

### B1. Normative standard

Review and accept `02-canonical-repository-standard.md`. Resolve mandatory versus recommended rules explicitly. Do not leave requirements ambiguous in prose.

### B2. Project profiles

Create profile files for:

1. single application/modular monolith;
2. monorepo;
3. data platform;
4. infrastructure.

Each profile should define:

- when to select it;
- recommended source layout;
- prohibited misleading structures;
- expected tests and operational evidence;
- profile-specific naming;
- allowed deviations.

### B3. Agent governance

Create the root `AGENTS.md`, safe default `.codex/config.toml`, three custom-agent roles, and three initial skills. Validate them against current Codex documentation before each standard release.

### B4. Pull-request evidence

Create a pull-request template that requires:

- user-facing summary;
- scope and non-goals;
- design and risk notes;
- test scenarios with expected and actual outcomes;
- migration, deployment, and rollback impact;
- documentation impact;
- agent/tool disclosure where material.

### B5. Documentation lifecycle

Create minimal templates for architecture, ADRs, runbooks, and exact reference documents. Do not pre-populate numerous empty documents.

### B6. Validator

Implement a dependency-free validator that checks objective repository rules. It should support:

```text
--root <path>
--strict
--json
```

Initial checks:

- required governance files;
- valid standard manifest;
- `AGENTS.md` byte budget;
- unexpected nested agent instruction files;
- legacy active instruction filenames;
- skill metadata and duplicate names;
- safe Codex defaults;
- pull-request template sections;
- tracked logs, secrets, caches, generated audit output, and temporary files;
- documentation metadata on authoritative documents where enabled.

The validator MUST distinguish errors from warnings and include remediation text. Its own tests MUST cover compliant, warning, and failing fixture repositories.

## Workstream C — Pilot the standard

Use two pilots.

### Pilot 1: small, healthy repository

Purpose: validate the new-repository path and identify unnecessary ceremony.

Measure:

- time to bootstrap;
- number of manual corrections;
- clarity of commands and contribution flow;
- validator false positives;
- skill trigger accuracy;
- PR evidence quality.

### Pilot 2: complex existing repository

Purpose: validate audit-first adaptation without destructive restructuring.

Select a repository that contains stale documentation, scripts, multiple entry points, or agent files. A complex legacy/candidate-replacement repository pair is a strong pilot after a read-only continuity audit.

Measure:

- whether Codex correctly preserves framework conventions;
- whether it avoids mass moves and renames;
- number of unknown scripts identified;
- reduction in always-loaded instruction size;
- ability of a fresh agent to trace one critical workflow;
- test and continuity gaps found;
- bootstrap diff size and unrelated-change rate.

### Pilot acceptance gates

Proceed to wider rollout only when:

1. both repositories pass the validator;
2. no production behavior was removed during bootstrap;
3. a fresh human or agent can locate commands, architecture, and safety constraints;
4. executor/reviewer handoffs produce actionable independent review;
5. no mandatory artifact lacks an owner;
6. optional tooling remains optional;
7. standard exceptions are explicit and bounded;
8. feedback has removed rules that create ceremony without risk reduction.

## Workstream D — Roll out across the machine

### D1. Inventory only

First generate a repository inventory beneath an explicitly supplied root directory. Record:

- path and remote;
- active branch and dirty state;
- language/framework/build system;
- repository profile candidate;
- current agent files, skills, hooks, and MCP configuration;
- risk class;
- standard version, if any;
- recommended rollout order.

Do not edit repositories during the inventory phase.

### D2. Prioritize

Recommended order:

1. inactive or low-risk repositories;
2. active development repositories with good tests;
3. complex but non-production repositories;
4. client-facing and production repositories;
5. legacy/lite continuity projects after evidence gates.

### D3. Bootstrap one repository at a time

For each repository:

1. confirm clean state or create a safe snapshot;
2. create a dedicated branch/worktree;
3. run read-only discovery;
4. propose the profile and exceptions;
5. apply the smallest compatible governance diff;
6. run project tests and the validator;
7. use an independent reviewer;
8. commit locally;
9. push/open a PR only when authorized.

Do not let one failed bootstrap contaminate another repository.

### D4. Record adoption

Maintain a machine-level inventory outside project repositories containing only non-secret metadata:

```text
repository path
standard version
profile
adoption status
last validation
next review
approved optional capabilities
```

Do not create one global `AGENTS.md` containing all project knowledge. Global instructions should remain limited to personal working preferences; project behavior belongs inside each repository.

## Workstream E — Optional capability trials

Trial optional capabilities after baseline rollout.

### Ponytail-derived review

Test an explicit overengineering review on selected pull requests. Compare useful findings, false positives, missed correctness issues, and whether it pressures the team to remove necessary controls. Admit it only as a supplemental review, not the final reviewer.

### Codebase Memory MCP

Use an isolated `CODEX_HOME` and preferably install or configure without automatically modifying every agent surface. Start with:

- one repository;
- explicit indexing;
- auto-watch off;
- read-only query tools;
- no graph-owned authoritative ADRs;
- an uninstall plan.

Benchmark at least ten representative tasks:

- locate an entry point;
- trace callers/callees;
- identify impact of a schema or interface change;
- find an existing implementation before adding code;
- locate dead or duplicated behavior.

Compare task accuracy, time, context usage, false confidence, setup cost, and stale-index behavior against native repository search. Accept only when measured value exceeds operational cost.

## Suggested pull-request sequence for the standard repository

| PR | Scope |
|---|---|
| 1 | Repository skeleton, ownership, versioning, README |
| 2 | Normative standard and profiles |
| 3 | `AGENTS.md`, Codex config, custom agents |
| 4 | Initial skills and trigger tests |
| 5 | PR template and documentation templates |
| 6 | Validator implementation and tests |
| 7 | New-repository pilot fixes |
| 8 | Existing-repository pilot fixes |
| 9 | Release `1.0.0` and machine rollout guide |

Each PR must remain independently reviewable. Do not combine the validator, all profiles, optional MCP installations, and a real project migration into one change.

## Definition of done

The standard itself is ready for `1.0.0` when:

- normative rules have owners and unambiguous requirement strength;
- the template generates a valid new repository;
- the bootstrap prompt safely adapts an existing repository;
- the validator is tested and produces useful remediation;
- two pilots meet the acceptance gates;
- the multi-agent protocol has been exercised on a real change;
- optional integrations are not required for baseline compliance;
- release, upgrade, exception, and rollback procedures are documented.

# Multi-Project Machine Rollout Plan

**Purpose:** Apply the repository standard across multiple local projects without creating one global context blob or making uncontrolled edits across the machine.

## Recommended machine model

Use three layers:

```text
minimal user-level Codex defaults
        +
repository-scoped standard/config/skills
        +
optional isolated CODEX_HOME profiles for experimental or privileged tools
```

Do not create one universal global `AGENTS.md` containing the architecture and commands of every project. That recreates the context-pollution problem across repositories.

## Suggested local layout

The exact directories are user-selected. A clear model is:

```text
~/Projects/                         # project repositories
~/RepositoryStandards/             # this standard kit/repository
~/.codex/                           # minimal normal profile
~/.codex-code-memory-trial/         # optional isolated experimental profile
~/.codex-production-ops/            # optional tightly controlled profile
~/.local/state/repo-standard/       # non-secret inventory and reports
```

Never put production credentials or client data in the standard inventory.

## Phase 1 — Inventory, no writes

Provide Codex an explicit parent directory. It must locate Git repositories without traversing unrelated system or secret directories.

For each repository collect:

```text
absolute path
repository name
remote URL names (not credentials)
current branch and commit
dirty/clean state
last commit date
languages/frameworks/package managers
candidate profile
CI/build/test indicators
current AGENTS/override/fallback files
current skills/custom agents/hooks/MCP
standard version, if present
risk classification
recommended rollout wave
```

Produce a machine inventory outside all repositories. Do not modify repositories in this phase.

## Phase 2 — Triage and rollout waves

### Wave 1: low-risk calibration

Use one small inactive or internal repository to calibrate the prompt, template, and validator.

### Wave 2: healthy active repositories

Select repositories with tests and known owners. Bootstrap one at a time and refine exceptions.

### Wave 3: complex existing repositories

Use audit-first mode. Separate governance setup from source restructuring. Preserve unknown scripts and stale evidence until callers and contracts are reconciled.

### Wave 4: production/client-facing repositories

Require explicit owner approval, backup/snapshot, independent review, and full relevant tests. No production connection is needed merely to add repository governance.

### Wave 5: experimental optional tools

Trial Codebase Memory, browser automation, database MCP, or hooks only after baseline compliance and per-project admission.

## Phase 3 — Per-repository bootstrap

For each repository:

1. open a fresh Codex session in that repository;
2. use the normal minimal profile unless the project has an approved isolated profile;
3. run the universal bootstrap prompt with the standard kit path;
4. create a dedicated branch/worktree;
5. audit first;
6. apply only compatible governance files;
7. run tests and validator;
8. use independent review;
9. commit locally;
10. update the machine inventory;
11. push/open a PR only under explicit repository authorization.

Never ask one agent session to edit many unrelated repositories in one continuous context. Use one coherent session per repository to avoid carrying assumptions across projects.

## Phase 4 — Global personal defaults

After the first pilots, create a minimal user-level `AGENTS.md` containing only durable personal behavior, for example:

```markdown
- Investigate current behavior before changing it.
- Prefer small, reversible, evidence-backed changes.
- Do not expose secrets or client data.
- Do not access production without explicit authorization.
- Run relevant validation and report actual results.
- Distinguish facts, inferences, and unknowns.
```

Do not copy the canonical repository standard into the global file. Repository-scoped instructions are versioned and reviewed with the code they govern.

## Phase 5 — Standard version tracking

Maintain a non-secret inventory such as:

```json
{
  "repositories": [
    {
      "path": "/absolute/path/project-a",
      "standard_version": "1.0.0",
      "profile": "single-application",
      "status": "baseline",
      "last_validated": "2026-08-15",
      "next_review": "2026-11-15",
      "optional_capabilities": []
    }
  ]
}
```

This inventory is operational metadata, not an instruction source. Codex should read the target repository itself before making decisions.

## Phase 6 — Upgrades

When a new standard version is released:

1. read the standard changelog;
2. identify affected repositories from the inventory;
3. dry-run the bootstrap/upgrade workflow on one pilot;
4. create one upgrade PR per repository;
5. preserve project exceptions;
6. run project validation;
7. update the manifest and inventory only after the change is accepted.

Do not automatically copy template files over local adaptations.

## Risk controls

- Explicit parent search root; no whole-disk traversal.
- No secret values in reports.
- No global installation of project-specific skills.
- One repository per session and branch.
- No changes to dirty repositories without a safe snapshot.
- No production action in baseline bootstrap.
- No optional MCP/hook/memory activation in the same change.
- Local commit by default; remote write only when authorized.
- Stop one repository's rollout when validation fails; continue only through a separate decision.

## Completion criteria

Machine rollout is healthy when:

- every active repository is inventoried;
- each adopted repository declares a standard version and profile;
- all baseline repositories pass their validator;
- global instructions remain minimal;
- project-specific context stays repository-scoped;
- experimental/privileged capabilities use isolated profiles;
- no repository was mass-restructured during bootstrap;
- maintenance dates and owners are recorded;
- upgrades are reviewable per-repository changes.

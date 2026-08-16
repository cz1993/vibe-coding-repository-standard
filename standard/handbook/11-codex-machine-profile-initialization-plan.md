# Codex Machine Profile Initialization Plan

**Purpose:** Establish a clean, minimal default Codex profile for a machine that hosts multiple unrelated projects.

## Recommended decision

Use one conservative normal profile and separate `CODEX_HOME` directories for experiments or privileged operations.

```text
normal profile              minimal global rules, no optional MCP/hooks/memory
code-memory trial profile   isolated experiment only
production-ops profile      separately controlled, explicit tasks only
```

Repository-specific commands, architecture, skills, and safety rules stay inside each repository. Do not make the global profile a catalog of all projects.

## Inputs

```text
TARGET_CODEX_HOME=<normal profile path, usually existing ~/.codex>
STANDARD_KIT_PATH=<this kit>
MODE=audit-only | backup-and-apply
```

## Phase 1 — Audit current profile

Inspect without exposing secrets:

- `AGENTS.md` or other global instruction files;
- `config.toml` and managed requirements;
- user-level skills;
- custom agents;
- hooks and hook scripts;
- MCP/app/plugin configuration;
- memory settings/data;
- unexpected fallback instruction names;
- file permissions and ownership.

Classify every item as keep, merge, isolate, disable, remove later, or unknown. Do not overwrite an existing profile blindly.

## Phase 2 — Backup

In apply mode, create a timestamped local backup outside project repositories. Preserve permissions. Do not place credentials or full secret-bearing configuration in a repository or report.

Record a restore command and verify the backup can be read by the current user only.

## Phase 3 — Apply minimal normal profile

Adapt `machine-profile/AGENTS.md` and `machine-profile/config.toml`.

The normal profile should contain:

- conservative approval/sandbox/network defaults;
- memories and hooks disabled;
- multi-agent enabled with small concurrency;
- automatic secret-name environment exclusions;
- no MCP servers or external integrations by default;
- no project-specific commands or architecture;
- no model pin unless the user intentionally chooses one.

Do not delete existing optional tools immediately. Move them to an isolated profile or leave disabled until their ownership and purpose are known.

## Phase 4 — Validate

- Parse the resulting TOML.
- Confirm the global `AGENTS.md` is small and project-neutral.
- Confirm no secrets were printed or copied.
- Confirm no project files were changed.
- Launch Codex in a disposable test repository and inspect the effective instruction/config behavior.
- Confirm repository-scoped configuration can add project rules without inheriting unrelated projects.

## Phase 5 — Create isolated profiles only as needed

An isolated profile requires:

- named purpose;
- owner;
- tools/capabilities;
- environments/data accessed;
- permission boundary;
- expiration/review date;
- uninstall/restore procedure.

Do not share a production-capable profile with ordinary coding sessions.

## Phase 6 — Report

Report:

- files backed up and changed;
- global instructions before/after size;
- enabled/disabled memories, hooks, MCP, skills, and custom agents;
- isolated profiles created;
- restore path and command;
- unresolved unknowns;
- validation performed.

## Definition of done

The machine profile is ready when a new Codex session starts with conservative universal behavior, no project-specific context, no unapproved external tool catalog, and a tested rollback path.

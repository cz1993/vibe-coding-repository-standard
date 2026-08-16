# Codex Prompt — Initialize a Clean Machine Profile

```text
Act as a cautious configuration migration orchestrator.

INPUTS

TARGET_CODEX_HOME=<absolute Codex profile path, usually ~/.codex>
STANDARD_KIT_PATH=<absolute path to vibe-coding-repository-standard>
BACKUP_ROOT=<absolute private local backup directory outside project repositories>
MODE=audit-only | backup-and-apply

DEFAULTS

- MODE=audit-only
- no project repository changes
- no network or external installer execution
- no secret values in output
- no deletion of unknown configuration
- no MCP, hook, memory, plugin, or project-specific skill installation

READ FIRST

- STANDARD_KIT_PATH/standard/handbook/11-codex-machine-profile-initialization-plan.md
- STANDARD_KIT_PATH/standard/handbook/06-agent-skill-mcp-governance.md
- STANDARD_KIT_PATH/standard/machine-profile/README.md
- STANDARD_KIT_PATH/standard/machine-profile/AGENTS.md
- STANDARD_KIT_PATH/standard/machine-profile/config.toml

GOAL

Create a conservative normal Codex profile for a machine with multiple projects while preserving a tested rollback path and keeping project-specific knowledge inside repositories.

1. AUDIT

Inspect TARGET_CODEX_HOME metadata and configuration without printing credentials or secret values. Inventory:

- global instruction files and byte sizes;
- config.toml and managed requirements;
- user-level skills and custom agents;
- hooks and scripts;
- MCP/apps/plugins and tool scopes;
- memory configuration/data;
- fallback instruction names;
- permissions/ownership;
- files whose purpose is unknown.

Classify each item: keep, merge, isolate into another CODEX_HOME, disable, candidate removal, or investigate.

2. PROPOSAL

Before any write, present:

- current risks and context-pollution sources;
- proposed minimal global AGENTS.md;
- proposed config merge;
- capabilities left disabled;
- items preserved or isolated;
- exact files to change;
- backup and restore plan;
- validation plan.

If MODE=audit-only, stop here and write no profile files.

3. BACKUP

When MODE=backup-and-apply:

- create a timestamped backup under BACKUP_ROOT;
- preserve permissions;
- restrict backup access to the current user where supported;
- do not copy the backup into Git or a project directory;
- record and verify the restore command.

4. APPLY

Merge the machine-profile templates. Do not overwrite useful existing settings blindly.

Required normal-profile outcome:

- global AGENTS.md contains only project-neutral personal defaults;
- approval on-request and workspace-write sandbox;
- workspace network disabled;
- memories and hooks disabled;
- multi-agent enabled with concurrency 3;
- automatic secret-name environment exclusions applied;
- no default MCP servers or external integrations;
- no project commands, architecture, client names, or task history;
- no model pin unless already intentionally approved and preserved with rationale.

Unknown or potentially useful optional tools should be disabled/preserved or moved to a proposed isolated profile, not destroyed.

5. VALIDATE

- Parse the resulting TOML with a standard parser.
- Confirm instruction size and project-neutral content.
- Confirm no secrets were printed or added.
- Confirm no project repository changed.
- Test the profile in a disposable repository and inspect effective behavior.
- Confirm the backup/restore path exists.

6. FINAL REPORT

Use plain language. Include:

- files backed up and changed;
- before/after instruction size;
- memories/hooks/MCP/skills/custom-agent state;
- preserved unknowns and recommended isolated profiles;
- validation results;
- backup and restore locations/commands;
- unresolved risks.

Do not claim optional tools are removed unless their processes, config, skills, hooks, and owned files were all verified.
```

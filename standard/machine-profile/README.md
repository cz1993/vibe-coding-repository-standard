# Minimal Codex Machine Profile

These files are reference inputs for `prompts/06-initialize-codex-machine-profile.prompt.md`. They must be merged with an existing profile after audit and backup; do not overwrite `~/.codex` blindly.

- `AGENTS.md`: durable personal working behavior only.
- `config.toml`: conservative normal-session defaults.

Project architecture, commands, skills, custom agents, and tool admissions belong inside each repository. Experimental or privileged integrations should use separate `CODEX_HOME` profiles.

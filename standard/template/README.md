# Project Name

**Status:** Active development  
**Owner:** Replace with the owning person or team  
**Repository profile:** Replace with `single-application`, `monorepo`, `data-platform`, or `infrastructure`

## Purpose

Explain in plain language:

- who uses this project;
- what outcome it provides;
- what is inside this repository;
- what is intentionally outside its scope.

## Safety and environment boundaries

State whether the project handles production systems, client data, personal data, credentials, paid APIs, scheduled jobs, or destructive migrations. Link to `SECURITY.md` and applicable runbooks.

## Getting started

Only include commands that have been executed successfully in the current repository.

```bash
# Replace or remove. Do not leave unverified examples.
```

The exact verified command register is maintained in [`docs/reference/commands.md`](docs/reference/commands.md).

## Repository map

Describe the actual top-level directories. Do not copy a generic tree that the repository does not use.

| Path | Purpose | Owner |
|---|---|---|
| `src/` | Replace with the actual purpose, or remove this row | Replace |
| `tests/` | Replace with the actual test organization | Replace |
| `docs/` | Architecture, decisions, runbooks, and reference | Replace |

## Architecture

Start with:

- [`docs/architecture/README.md`](docs/architecture/README.md)
- [`docs/decisions/`](docs/decisions/)

Keep architecture claims linked to code, configuration, tests, or runtime evidence.

## Development and review

- Repository instructions: [`AGENTS.md`](AGENTS.md)
- Contribution process: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Pull requests must show material test scenarios, expected results, actual results, and evidence.
- Use independent review for non-trivial changes.

## Operations

Operational procedures belong in [`docs/runbooks/`](docs/runbooks/). Exact commands, contracts, and schemas belong in [`docs/reference/`](docs/reference/).

## Repository standard

This repository declares its standard version, profile, active skills, and exceptions in [`.repo-standard.json`](.repo-standard.json).

Validate the governance surface with:

```bash
python scripts/maintenance/validate_repository_standard.py --root .
```

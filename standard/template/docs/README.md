# Documentation Map

**Status:** Authoritative  
**Owner:** Replace with repository governance owner  
**Last validated:** 2026-08-15  
**Validated by:** repository structure and standard validator

Use the smallest document type that answers the reader's need.

| Location | Purpose | Typical question |
|---|---|---|
| `architecture/` | System context, boundaries, and important flows | How does the system fit together? |
| `decisions/` | Durable choices, tradeoffs, and consequences | Why did we choose this? |
| `runbooks/` | Human operational procedures | How do I operate or recover it? |
| `reference/` | Exact commands, contracts, schemas, and APIs | What is the precise interface or command? |

Tutorials or onboarding guides may be added when a real audience needs them. Do not create empty documentation categories or copy facts into several files.

## Document header

Authoritative documents should begin with:

```text
Status: Draft | Authoritative | Generated | Superseded
Owner: <role/team>
Last validated: YYYY-MM-DD
Validated by: <tests/config/commands/evidence>
Supersedes: <optional>
```

## Lifecycle

- Link claims to executable evidence where possible.
- Update docs with the behavior they describe.
- Delete superseded active documents after unique current information and retention needs are reconciled.
- Use Git history as the default archive.
- Keep legal, contractual, client, and incident evidence in an approved external retention location that normal agents do not treat as current instructions.
- Mark generated documents and their generation command; never hand-maintain them.

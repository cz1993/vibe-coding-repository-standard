# Verified Command Register

**Status:** Draft until commands are executed  
**Owner:** Replace  
**Last validated:** 2026-08-15  
**Validated by:** command execution in the supported local/CI environment

Only record commands that have run successfully. Include environment, expected effect, external side effects, and date.

| Purpose | Command | Environment | Side effects/network | Last verified | Evidence |
|---|---|---|---|---|---|
| Validate repository standard | `python scripts/maintenance/validate_repository_standard.py --root .` | Python 3.11+ | local read-only | 2026-08-15 | validator output |

Remove template rows that do not apply. Do not copy commands from stale docs without executing them.

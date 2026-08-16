# Security Policy

## Supported versions

VCRS is currently a public preview.

| Version | Security updates |
|---|---|
| `0.1.x` | Supported |
| Earlier private drafts | Not supported |

## Reporting a vulnerability

Do not disclose a suspected vulnerability in a public issue, Discussion, pull request, log, or screenshot.

Use GitHub's **private vulnerability reporting** feature from the repository's Security tab. Maintainers should enable this feature when the repository is published.

If private vulnerability reporting is not available, open a public issue containing only this sentence:

> Private security contact requested.

Do not include technical details. A maintainer will arrange a private channel.

## What is in scope

Security reports may concern:

- the validators or release scripts;
- unsafe commands in prompts or examples;
- accidental secret or private-data exposure;
- dangerous default permissions;
- workflow or dependency risks;
- instructions that could unexpectedly access production, external services, or destructive operations;
- ways the standard encourages an agent to bypass authorization or review.

VCRS is primarily documentation and tooling. A weakness in an adopter's application is not automatically a VCRS vulnerability unless the standard or included code directly caused or recommended the unsafe behavior.

## Response goals

Maintainers aim to:

1. acknowledge a complete report promptly;
2. confirm scope and reproduce the issue where possible;
3. communicate expected next steps;
4. prepare a fix and release note before public disclosure when appropriate;
5. credit the reporter unless anonymity is requested.

No fixed response-time guarantee is made during public preview.

## Security expectations for contributors

- Never commit credentials, tokens, private keys, production records, client data, or personal data.
- Use synthetic fixtures.
- Keep GitHub Actions permissions minimal.
- Treat copied terminal output, prompts, and screenshots as potential sensitive-data sources.
- Avoid unreviewed `curl | shell` installation examples.
- Separate read-only investigation from mutating operations.
- Require explicit authorization for production, deployment, migration, deletion, and paid external-service actions.

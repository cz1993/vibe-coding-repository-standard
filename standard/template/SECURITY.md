# Security Policy

## Reporting a vulnerability

Replace this section with the approved private reporting channel. Do not ask reporters to place vulnerability details in a public issue.

## Security expectations

- Do not commit secrets, credentials, client data, production records, or private keys.
- Use synthetic or approved sanitized test fixtures.
- Apply least privilege to databases, cloud resources, MCP servers, agents, and CI credentials.
- Keep read and write capabilities separate where practical.
- Require explicit authorization for production, deployment, migration, deletion, and schedule changes.
- Preserve tenant/client isolation in authorization and data-access tests.
- Redact sensitive values from logs, prompts, reports, screenshots, and test output.
- Rotate and remediate any exposed credential; deleting the current file alone is not sufficient.

## Supported versions

Replace with the project's actual support and patch policy.

## Incident handling

Link approved incident, credential-rotation, backup/restore, and recovery runbooks from `docs/runbooks/`.

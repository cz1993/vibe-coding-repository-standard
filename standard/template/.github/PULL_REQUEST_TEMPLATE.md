## Plain-language summary

What user or operational outcome does this change provide? Explain it without relying on internal jargon.

## Scope and non-goals

**In scope**

-

**Not in scope**

-

## Design and behavior

- Current behavior:
- New behavior:
- Relevant entry point/data flow:
- Why this is the smallest defensible change:
- New dependency/abstraction/service: none, or explain the current need:

## Test evidence

| Scenario or risk | Setup/input | Expected result | Actual result | Evidence/command |
|---|---|---|---|---|
| Happy path |  |  |  |  |
| Boundary/edge |  |  |  |  |
| Failure/regression |  |  |  |  |

**Tests not run and why:**

## Risk and operational impact

- Security/privacy/tenant impact:
- Data/schema/API/file-contract impact:
- Concurrency/retry/idempotency impact:
- Deployment/schedule/external-service impact:
- Observability and failure-recovery impact:
- Rollback or forward-recovery plan:

## Documentation and governance

- Authoritative docs changed:
- Docs reviewed but unchanged:
- `AGENTS.md`, skill, custom-agent, MCP, memory, or hook impact:
- Standard exception added/closed:

## Agent/tool disclosure

- Executor:
- Independent reviewer:
- External tools/MCP used:
- Human verification performed:

## Checklist

- [ ] The change has one coherent purpose.
- [ ] Relevant entry points, callers, inputs, outputs, and side effects were traced.
- [ ] No unrelated cleanup or broad formatting is mixed in.
- [ ] Material test scenarios show expected and actual results.
- [ ] Generated tests were reviewed for useful failure behavior.
- [ ] No secrets, client data, logs, caches, or temporary artifacts were added.
- [ ] Production/deployment/migration actions were not performed without explicit authorization.
- [ ] Documentation changed only where the contract, decision, command, or operation changed.
- [ ] The complete diff was reviewed.
- [ ] An independent reviewer checked non-trivial changes.

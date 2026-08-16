# Ready-to-run Codex prompts

These prompts translate VCRS guidance into bounded workflows. Review the variables and safety defaults before running one. Do not grant production or destructive access merely because a prompt mentions an operation.

| Prompt | Use it for | Default posture |
|---|---|---|
| [`00-machine-wide-rollout.prompt.md`](00-machine-wide-rollout.prompt.md) | Inventory several local repositories and plan rollout waves | Inventory only |
| [`01-bootstrap-repository.prompt.md`](01-bootstrap-repository.prompt.md) | Audit and add a minimal governance baseline to one repository | Audit, then bounded apply |
| [`02-multi-agent-change-cycle.prompt.md`](02-multi-agent-change-cycle.prompt.md) | Run a normal executor/reviewer development cycle | Small scoped change |
| [`03-quarterly-governance-review.prompt.md`](03-quarterly-governance-review.prompt.md) | Review agent files, skills, docs, scripts, and optional capabilities | Read-first maintenance |
| [`04-codebase-memory-admission-trial.prompt.md`](04-codebase-memory-admission-trial.prompt.md) | Measure whether structural code indexing earns its cost and permissions | Isolated trial |
| [`05-overengineering-review-trial.prompt.md`](05-overengineering-review-trial.prompt.md) | Add a supplemental minimal-change review | Read-only |
| [`06-initialize-codex-machine-profile.prompt.md`](06-initialize-codex-machine-profile.prompt.md) | Audit and establish a conservative machine-level Codex profile | Audit only |

Use one coherent prompt per task. The prompts are a reference implementation, not a substitute for reading the target repository's own instructions and evidence.

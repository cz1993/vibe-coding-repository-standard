---
name: safe-change
description: Trace, implement, test, and independently review one bounded software change. Use for ordinary feature, bug-fix, or refactor work after the repository is bootstrapped; do not use for broad repository cleanup, production operations, or undefined rewrites.
---

# Safe Change

## Inputs

- user outcome;
- in-scope behavior/modules;
- explicit non-goals;
- acceptance criteria;
- safety and environment restrictions;
- Git action.

## Method

1. Trace the current entry point, callers, inputs, outputs, dependencies, and side effects.
2. Locate existing code, configuration, tests, and platform facilities before adding anything.
3. Define the smallest defensible change and test scenarios.
4. Implement only the accepted scope.
5. Prefer, in order:
   - existing repository behavior;
   - language/runtime standard facilities;
   - framework/platform features;
   - already-installed dependencies;
   - direct code;
   - a new abstraction or dependency only with current evidence.
6. Never simplify away validation, security, privacy, data isolation, error handling, observability, accessibility, migration safety, recovery, or useful tests.
7. Add tests at the smallest credible level and cover important boundaries with integration/contract/smoke evidence as applicable.
8. Review the complete diff and remove unrelated changes.
9. Prepare a test table showing scenario, input/setup, expected, actual, and evidence.
10. Use an independent read-only reviewer for non-trivial changes; resolve and recheck blockers.

## Output

Report in plain language:

- what changed and why;
- files changed;
- behavior before/after;
- tests and actual outcomes;
- reviewer findings and resolutions;
- unrun validation and residual risk;
- commit/PR identifiers.

Do not expose internal scratchpads or agent transcripts.

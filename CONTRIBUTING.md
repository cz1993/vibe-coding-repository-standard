# Contributing to VCRS

Thank you for helping make AI-assisted software easier to understand and maintain.

VCRS welcomes contributions from experienced engineers, new vibe coders, technical writers, security reviewers, researchers, and coding-agent tool builders.

## Good first contributions

- clarify a confusing paragraph;
- report a broken link or inaccurate command;
- improve an example for a beginner;
- add a test for the validator;
- share a sanitized adoption case and what did or did not work;
- propose a repository profile backed by real projects;
- test one VCRS workflow with a non-Codex coding agent;
- improve accessibility, diagrams, or navigation.

## Before starting a larger change

Open an issue or Discussion before making a substantial normative change, new adapter, new profile, or broad restructuring. Explain:

- the user problem;
- current evidence;
- the proposed outcome;
- compatibility and migration impact;
- alternatives considered;
- how the result can be tested.

This prevents contributors from investing in a direction that does not fit the standard.

## Development setup

VCRS has no runtime dependency for its validators. Python 3.11 or newer is recommended.

Run the public repository checks:

```bash
python -m unittest discover -s tests/quality -p 'test_*.py' -v
python scripts/quality/validate_public_repository.py --root . --strict
python scripts/quality/audit_publication.py --root . --strict
```

Run the starter-template checks:

```bash
python standard/template/scripts/maintenance/validate_repository_standard.py \
  --root standard/template

python -m unittest discover \
  -s standard/template/tests/standards \
  -p 'test_*.py' \
  -v
```

## Change principles

- Trace the current behavior before changing it.
- Keep one pull request focused on one coherent outcome.
- Separate structural changes from normative behavior changes where practical.
- Prefer plain language over unexplained jargon.
- Do not create abstractions or files “for future use” without a present requirement.
- Preserve useful safety controls, tests, migration evidence, and attribution.
- Do not introduce a new dependency when the standard library is sufficient.
- Do not claim compatibility with an agent or platform without testing it.
- Never include private repository content, client data, credentials, or identifying logs in an issue or pull request.

## Pull-request evidence

Use the pull-request template. For material behavior, validator, prompt, or workflow changes, include test scenarios in this form:

| Scenario | Setup or input | Expected result | Actual result | Evidence |
|---|---|---|---|---|
| Example | Example | Example | Example | Command, test, screenshot, or report |

List any tests not run and why. A green CI result does not replace explaining what the tests prove.

## Normative language

The detailed standard uses:

- **MUST / MUST NOT** for mandatory compatibility or safety requirements;
- **SHOULD / SHOULD NOT** for strong recommendations with valid exceptions;
- **MAY** for optional behavior.

A proposal that changes normative language should explain adoption and migration impact.

## Review

A non-trivial change should receive independent review. Reviewers prioritize:

1. correctness and misleading claims;
2. security, privacy, and sensitive-data exposure;
3. compatibility and migration impact;
4. regressions in validators, prompts, links, or templates;
5. evidence quality;
6. clarity for the intended audience;
7. maintainability and unnecessary complexity.

Preference-only comments are non-blocking unless they reflect an accepted project convention.

## Commit and attribution

By submitting a contribution, you agree that it may be distributed under the project's Apache-2.0 license. Keep commits understandable and do not rewrite shared history without maintainer agreement.

## Community expectations

Read and follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). Use [`SECURITY.md`](SECURITY.md) for vulnerabilities and [`SUPPORT.md`](SUPPORT.md) for help requests.

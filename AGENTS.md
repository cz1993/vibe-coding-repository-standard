# VCRS Repository Instructions

## Purpose

This repository publishes the Vibe Coding Repository Standard (VCRS), its Codex-first reference implementation, prompts, templates, validators, and public documentation.

## Communication

- Write in plain, direct, user-friendly language.
- Explain unavoidable jargon or link to `docs/glossary.md`.
- Distinguish confirmed facts, evidence-backed inferences, proposals, and unknowns.
- Do not overstate compatibility, production readiness, benchmarks, adoption, or search visibility.
- When a change affects behavior, show the important test scenarios, expected outcomes, actual outcomes, commands, and evidence in the pull request.
- State which checks were not run and why. Do not write “all tests pass” without supporting output.

## Change discipline

Before editing, classify the change as editorial, implementation, normative, security-related, or release-related.

- Trace current links, validators, prompts, and version references before changing them.
- Keep one pull request focused on one coherent outcome.
- Preserve meaning during moves; separate broad structural changes from normative changes.
- Prefer the smallest defensible solution and the Python standard library.
- Do not add a dependency, agent capability, MCP server, hook, or memory feature without a demonstrated need, owner, risk boundary, and removal plan.
- Do not copy third-party text or code without checking its license and recording required attribution.
- The executor may validate its own work, but a material change requires independent review before approval.

## Privacy and safety

- Never add private repository content, client or employer data, personal data, credentials, internal domains, or identifying logs.
- Use synthetic examples and clearly fake values.
- Do not run included prompts against production or paid external systems during repository maintenance.
- Do not publish security details in a public issue, Discussion, pull request, screenshot, or log.

## Validation

Run the checks relevant to the change. The full local suite is:

```bash
python -m unittest discover -s tests/quality -p 'test_*.py' -v
python scripts/quality/validate_public_repository.py --root . --strict
python scripts/quality/audit_publication.py --root . --strict
python -m unittest discover -s standard/template/tests/standards -p 'test_*.py' -v
python standard/template/scripts/maintenance/validate_repository_standard.py \
  --root standard/template
```

For a release candidate, also run the publication audit with a private deny-term file stored outside this repository, then build the archive with `scripts/release/build_release.py`.

## Sources of truth

- Public identity and entry path: `README.md`
- Product rationale: `WHITEPAPER.md`
- Normative requirements: `standard/handbook/02-canonical-repository-standard.md`
- Governance: `GOVERNANCE.md`
- Release history and version: `CHANGELOG.md` and `VERSION`
- Public-readiness findings: `docs/publication-audit.md`
- Detailed research sources: `standard/handbook/09-source-register.md`

Do not treat generated artifacts, old chats, temporary audit output, or agent memory as authoritative documentation.

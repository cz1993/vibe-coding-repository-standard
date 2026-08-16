# Publishing checklist

This package is prepared to become a new public GitHub repository. Repository ownership, Git author identity, security settings, and the final push still require an authenticated maintainer.

## Recommended repository identity

- **Name:** `vibe-coding-repository-standard`
- **Visibility:** public
- **Default branch:** `main`
- **Description:** Open-source repository standard, starter template, validator, and multi-agent workflow for making vibe-coded and AI-generated software understandable, testable, reviewable, and maintainable.
- **License:** Apache-2.0
- **Initial release:** `v0.1.0` public preview
- **Social preview:** `assets/social-preview.png`

Use the topics and launch guidance in [`docs/discovery-and-launch.md`](docs/discovery-and-launch.md).

## Before the first commit

- [ ] Create a new empty public repository; do not import private Git history.
- [ ] Confirm the GitHub account or organization that should own the public project.
- [ ] Confirm the Git author name and email that will appear permanently in public history.
- [ ] Recheck the desired repository slug and basic trademark risk.
- [ ] Run every local verification command below.
- [ ] Read [`docs/publication-audit.md`](docs/publication-audit.md).
- [ ] Review all files staged for the initial commit.
- [ ] Confirm that no local edit added names, client data, private paths, logs, credentials, or internal domains.

## Local verification

```bash
python -m unittest discover -s tests/quality -p 'test_*.py' -v
python scripts/quality/validate_public_repository.py --root . --strict
python scripts/quality/audit_publication.py --root . --strict
python -m unittest discover \
  -s standard/template/tests/standards \
  -p 'test_*.py' \
  -v
python standard/template/scripts/maintenance/validate_repository_standard.py \
  --root standard/template
```

For the last privacy check, use an external private deny-term file:

```bash
python scripts/quality/audit_publication.py \
  --root . \
  --strict \
  --deny-term-file ../private-publication-deny-terms.txt
```

Do not commit that file.

## Build the release archive

```bash
python scripts/release/build_release.py \
  --root . \
  --output-dir ../release \
  --deny-term-file ../private-publication-deny-terms.txt
```

The builder validates the repository, audits it again, creates a deterministic ZIP, places `FILE-MANIFEST.sha256` inside the archive, and writes a separate ZIP checksum.

## Initialize the public Git history

Run these commands from the sanitized package, replacing only the public remote URL:

```bash
git init -b main
git add .
git status --short
git diff --cached --stat
git diff --cached
git commit -m "Publish VCRS 0.1.0 public preview"
git remote add origin <PUBLIC_REPOSITORY_URL>
git push -u origin main
```

Do not use `git filter-branch`, subtree merges, or a private repository mirror as a shortcut for this first public release. Starting from the sanitized package is simpler and safer.

## GitHub settings after the first push

- [ ] Add the repository description and reviewed topics.
- [ ] Upload `assets/social-preview.png` in repository settings.
- [ ] Enable Issues.
- [ ] Enable Discussions when moderation capacity exists.
- [ ] Enable private vulnerability reporting.
- [ ] Enable secret scanning, push protection, Dependabot alerts, and security updates where available.
- [ ] Keep default GitHub Actions token permissions read-only.
- [ ] Require approval for workflows from first-time contributors.
- [ ] Add a default-branch ruleset requiring the VCRS quality workflow and pull-request review.
- [ ] Disable force pushes and branch deletion on `main`.
- [ ] Review GitHub's Community Standards page to confirm the health files are detected.
- [ ] Consider requiring third-party Actions to be pinned to immutable full commit SHAs as the project matures.

The root repository is the VCRS product and documentation source. Do **not** enable it as a template repository merely because it contains a starter. Adopters should use [`standard/template/`](standard/template/) until a dedicated application-template repository exists.

## Initial GitHub release

- [ ] Review [`CHANGELOG.md`](CHANGELOG.md).
- [ ] Create annotated tag `v0.1.0` from the audited commit.
- [ ] Create release title: `VCRS 0.1.0 — From vibes to verifiable software`.
- [ ] Mark it clearly as a public preview.
- [ ] Attach the deterministic ZIP and its `.sha256` file.
- [ ] Link the README, white paper, getting-started guide, FAQ, roadmap, and publication audit.
- [ ] Describe tested compatibility narrowly: principles are portable; the included implementation is Codex-first.

## After launch

- [ ] Verify the rendered SVG, Mermaid diagrams, tables, and relative links on GitHub.
- [ ] Test the bootstrap prompt in a clean sample repository.
- [ ] Pin a “Start here” Discussion when Discussions are enabled.
- [ ] Invite reports about confusing, overly rigid, unsafe, or unnecessary requirements.
- [ ] Collect measurable adoption evidence before making productivity or quality claims.
- [ ] Follow the ethical launch sequence in `docs/discovery-and-launch.md` rather than mass-posting identical promotion.

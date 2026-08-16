# Release guide

## Release roles

Assign one release steward and at least one independent reviewer. The steward prepares the release; the reviewer checks the final diff, audit evidence, and archive.

## Prepare

1. Confirm the intended version in `VERSION`.
2. Update `CHANGELOG.md`, `CITATION.cff`, README badges, standard manifest, and normative handbook version.
3. Review compatibility and migration impact.
4. Refresh sources whose behavior may have changed.
5. Confirm all new files are intentional and licensed.

## Validate

Run:

```bash
python -m unittest discover -s standard/template/tests/standards -p 'test_*.py' -v
python standard/template/scripts/maintenance/validate_repository_standard.py --root standard/template
python -m unittest discover -s tests/quality -p 'test_*.py' -v
python scripts/quality/validate_public_repository.py --root . --strict
python scripts/quality/audit_publication.py --root . --strict
```

Also review:

- rendered README and Mermaid diagrams;
- social-preview image dimensions and readability;
- Community Standards files;
- all GitHub Actions permissions;
- full Git history with a dedicated secret scanner when history exists;
- exact release archive contents and checksum.

## Package

Create a clean archive from the audited commit rather than zipping a working directory with caches or local metadata. Use normalized timestamps and permissions when producing a reproducible package.

Use `scripts/release/build_release.py` to create the archive. The builder writes a `FILE-MANIFEST.sha256` inside the ZIP and a separate checksum for the ZIP; the source tree intentionally does not track a self-invalidating manifest.

## Review

The independent reviewer checks:

- version consistency;
- sensitive-information and credential findings;
- broken links and commands;
- public/private boundary;
- third-party notices and license;
- compatibility and marketing claims;
- generated archive contents;
- test and audit results;
- rollback or correction plan.

## Publish

After approval:

1. merge to the protected default branch;
2. create a signed or verified tag when available;
3. create a GitHub Release with concise notes and known limitations;
4. attach the normalized ZIP and checksum;
5. verify the public repository's README, license, citation, community profile, security form, and social preview;
6. announce the release using the discovery guide.

## After release

- monitor security reports and broken setup paths;
- label `good first issue` candidates;
- collect adoption evidence;
- correct misleading claims promptly;
- schedule the next source and governance review.

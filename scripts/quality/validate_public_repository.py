#!/usr/bin/env python3
"""Validate the public VCRS repository package using the Python standard library.

The validator checks repository completeness, internal links, identity/version
consistency, parseable machine-readable files, safe release hygiene, and the
included visual assets. It does not prove that the standard is correct, secure,
or compatible with every coding agent.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys
import tomllib
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Sequence

STANDARD_ID = "VCRS-1"
PROJECT_NAME = "Vibe Coding Repository Standard"
PROJECT_SLUG = "vibe-coding-repository-standard"

REQUIRED_FILES = (
    "README.md",
    "WHITEPAPER.md",
    "LICENSE",
    "NOTICE",
    "ACKNOWLEDGEMENTS.md",
    "VERSION",
    "CHANGELOG.md",
    "ROADMAP.md",
    "CITATION.cff",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "SECURITY.md",
    "SUPPORT.md",
    "THIRD_PARTY_NOTICES.md",
    "PUBLISHING.md",
    "llms.txt",
    "AGENTS.md",
    ".repo-standard.json",
    ".codex/config.toml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/quality.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "assets/vcrs-hero.svg",
    "assets/vcrs-logo.svg",
    "assets/social-preview.png",
    "docs/getting-started.md",
    "docs/faq.md",
    "docs/glossary.md",
    "docs/publication-audit.md",
    "docs/discovery-and-launch.md",
    "standard/README.md",
    "standard/handbook/README.md",
    "standard/prompts/README.md",
    "standard/handbook/02-canonical-repository-standard.md",
    "standard/handbook/09-source-register.md",
    "standard/template/AGENTS.md",
    "standard/template/.repo-standard.json",
    "standard/template/scripts/maintenance/validate_repository_standard.py",
    "scripts/quality/audit_publication.py",
    "scripts/release/build_release.py",
)

REQUIRED_ISSUE_FORMS = (
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/documentation.yml",
    ".github/ISSUE_TEMPLATE/feature.yml",
)

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
}

GENERATED_OR_PRIVATE_NAMES = {
    ".DS_Store",
    "Thumbs.db",
}

GENERATED_OR_PRIVATE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
    ".bak",
    ".swp",
    ".zip",
    ".tar",
    ".tgz",
    ".gz",
}

LEGACY_TERMS = (
    "Codex Repository " + "Standard Kit",
    "codex-repository-" + "standard-kit",
    "1.0.0-" + "draft",
    "docs/" + "assets/",
)

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)")
HTML_LINK_RE = re.compile(r"\b(?:src|href)=[\"']([^\"']+)[\"']", re.IGNORECASE)
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


@dataclass(frozen=True)
class Finding:
    severity: str  # error | warning | info
    code: str
    path: str
    message: str
    line: int | None = None
    remediation: str = ""


def _iter_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        base = Path(current)
        for name in sorted(files):
            yield base / name


def _rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _finding(
    severity: str,
    code: str,
    path: str,
    message: str,
    line: int | None = None,
    remediation: str = "",
) -> Finding:
    return Finding(severity, code, path, message, line, remediation)


def _strip_code_fences(text: str) -> list[tuple[int, str]]:
    """Return non-fenced lines while preserving original line numbers."""
    output: list[tuple[int, str]] = []
    fence: str | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        marker = None
        if stripped.startswith("```"):
            marker = "```"
        elif stripped.startswith("~~~"):
            marker = "~~~"
        if marker:
            if fence is None:
                fence = marker
            elif fence == marker:
                fence = None
            continue
        if fence is None:
            output.append((number, line))
    return output


def _normalize_link_target(raw: str) -> str:
    target = raw.strip().strip("<>")
    if target.startswith("./"):
        target = target[2:]
    return target


def _is_external_or_anchor(target: str) -> bool:
    lower = target.lower()
    return (
        not target
        or target.startswith("#")
        or lower.startswith(("http://", "https://", "mailto:", "tel:", "data:"))
        or target.startswith("//")
        or "{{" in target
        or "}}" in target
    )


def _resolve_local_link(source: Path, target: str, root: Path) -> Path | None:
    clean = target.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return source
    # Reject absolute filesystem paths while allowing repository-root-relative links.
    if clean.startswith("/"):
        candidate = root / clean.lstrip("/")
    else:
        candidate = source.parent / clean
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None
    return resolved


def check_required_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for relative in (*REQUIRED_FILES, *REQUIRED_ISSUE_FORMS):
        if not (root / relative).is_file():
            findings.append(
                _finding(
                    "error",
                    "required-file-missing",
                    relative,
                    "Required public-release file is missing.",
                    remediation="Restore or intentionally redesign the release surface and update the validator.",
                )
            )
    return findings


def check_generated_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_files(root):
        rel = _rel(path, root)
        name = path.name
        if name in GENERATED_OR_PRIVATE_NAMES or path.suffix.lower() in GENERATED_OR_PRIVATE_SUFFIXES:
            findings.append(
                _finding(
                    "error",
                    "generated-or-private-file",
                    rel,
                    "Generated, archive, editor, or transient file is present in the publishable source tree.",
                    remediation="Remove it from the source tree and keep release artifacts outside the repository or under an ignored output directory.",
                )
            )
        if "__pycache__" in path.parts:
            findings.append(
                _finding(
                    "error",
                    "python-cache",
                    rel,
                    "Python bytecode cache is present.",
                    remediation="Delete cache directories before publication.",
                )
            )
    return findings


def check_identity_and_version(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    version_path = root / "VERSION"
    if not version_path.is_file():
        return findings
    version = version_path.read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(version):
        findings.append(
            _finding(
                "error",
                "invalid-version",
                "VERSION",
                f"VERSION is not a supported semantic version: {version!r}.",
            )
        )
        return findings

    expected_checks = {
        "README.md": (PROJECT_NAME, f"version-{version}"),
        "WHITEPAPER.md": (PROJECT_NAME, version),
        "CHANGELOG.md": (f"[{version}]",),
        "CITATION.cff": (PROJECT_NAME, f"version: {version}"),
        ".repo-standard.json": (STANDARD_ID, f'"version": "{version}"'),
        "standard/handbook/02-canonical-repository-standard.md": (STANDARD_ID, f"**Version:** {version}"),
    }
    for relative, needles in expected_checks.items():
        path = root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                findings.append(
                    _finding(
                        "error",
                        "identity-version-mismatch",
                        relative,
                        f"Expected project identity/version marker is missing: {needle!r}.",
                        remediation="Update the file so project name, standard ID, and release version are consistent.",
                    )
                )

    manifest_path = root / ".repo-standard.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("standard", {}).get("id") != STANDARD_ID:
                raise ValueError("standard.id mismatch")
            if manifest.get("standard", {}).get("version") != version:
                raise ValueError("standard.version mismatch")
            if manifest.get("repository", {}).get("name") != PROJECT_SLUG:
                raise ValueError("repository.name mismatch")
        except (json.JSONDecodeError, ValueError) as exc:
            findings.append(
                _finding(
                    "error",
                    "manifest-identity-mismatch",
                    ".repo-standard.json",
                    f"Public repository manifest is inconsistent: {exc}.",
                )
            )

    for path in _iter_files(root):
        if path.suffix.lower() not in {".md", ".txt", ".json", ".toml", ".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for term in LEGACY_TERMS:
            if term in text:
                findings.append(
                    _finding(
                        "error",
                        "legacy-publication-term",
                        _rel(path, root),
                        f"Legacy publication path or draft identity remains: {term!r}.",
                        remediation="Replace the stale reference with the current VCRS public path or version.",
                    )
                )
    return findings


def check_markdown_links(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[tuple[str, int, str]] = set()
    for source in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in source.parts):
            continue
        rel_source = _rel(source, root)
        text = source.read_text(encoding="utf-8", errors="replace")
        for line_number, line in _strip_code_fences(text):
            targets = [match.group(1) for match in MARKDOWN_LINK_RE.finditer(line)]
            targets.extend(match.group(1) for match in HTML_LINK_RE.finditer(line))
            ref = REFERENCE_LINK_RE.match(line)
            if ref:
                targets.append(ref.group(1))
            for raw_target in targets:
                target = _normalize_link_target(raw_target)
                if _is_external_or_anchor(target):
                    continue
                key = (rel_source, line_number, target)
                if key in seen:
                    continue
                seen.add(key)
                resolved = _resolve_local_link(source, target, root)
                if resolved is None:
                    findings.append(
                        _finding(
                            "error",
                            "link-escapes-repository",
                            rel_source,
                            f"Relative link leaves the repository: {target!r}.",
                            line_number,
                        )
                    )
                elif not resolved.exists():
                    findings.append(
                        _finding(
                            "error",
                            "broken-relative-link",
                            rel_source,
                            f"Relative link target does not exist: {target!r}.",
                            line_number,
                            remediation="Correct the path or remove the stale link.",
                        )
                    )
    return findings


def _yaml_surface_check(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = _rel(path, root)
    text = path.read_text(encoding="utf-8", errors="replace")
    for number, line in enumerate(text.splitlines(), start=1):
        if "\t" in line:
            findings.append(
                _finding(
                    "error",
                    "yaml-tab-indentation",
                    rel,
                    "YAML contains a tab character; GitHub configuration should use spaces.",
                    number,
                )
            )
    if path.name == "CITATION.cff":
        for key in ("cff-version:", "title:", "type:", "authors:", "version:", "license:"):
            if key not in text:
                findings.append(
                    _finding("error", "citation-field-missing", rel, f"CITATION.cff is missing {key!r}.")
                )
    if ".github/ISSUE_TEMPLATE" in rel and path.name != "config.yml":
        for key in ("name:", "description:", "body:"):
            if key not in text:
                findings.append(
                    _finding("error", "issue-form-field-missing", rel, f"Issue form is missing {key!r}.")
                )
    if rel.startswith(".github/workflows/"):
        if "permissions:" not in text or "contents: read" not in text:
            findings.append(
                _finding(
                    "error",
                    "workflow-permissions",
                    rel,
                    "Workflow does not declare read-only contents permission.",
                    remediation="Declare minimal permissions explicitly.",
                )
            )
    return findings


def check_machine_readable_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in _iter_files(root):
        rel = _rel(path, root)
        suffix = path.suffix.lower()
        try:
            if suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif suffix == ".toml":
                with path.open("rb") as handle:
                    tomllib.load(handle)
            elif suffix == ".py":
                compile(path.read_text(encoding="utf-8"), rel, "exec")
            elif suffix == ".svg":
                ET.parse(path)
            elif suffix in {".yml", ".yaml"} or path.name == "CITATION.cff":
                findings.extend(_yaml_surface_check(path, root))
        except (json.JSONDecodeError, tomllib.TOMLDecodeError, SyntaxError, ET.ParseError, UnicodeError) as exc:
            findings.append(
                _finding(
                    "error",
                    "machine-readable-parse-error",
                    rel,
                    f"File could not be parsed or compiled: {exc}.",
                )
            )
    return findings


def _read_png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("not a valid PNG header")
    return struct.unpack(">II", data[16:24])


def _png_metadata_chunks(path: Path) -> set[str]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return set()
    chunks: set[str] = set()
    position = 8
    while position + 12 <= len(data):
        length = int.from_bytes(data[position : position + 4], "big")
        chunk_type = data[position + 4 : position + 8]
        if chunk_type in {b"tEXt", b"zTXt", b"iTXt", b"eXIf"}:
            chunks.add(chunk_type.decode("ascii"))
        position += 12 + length
        if chunk_type == b"IEND":
            break
    return chunks


def check_assets(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    social = root / "assets/social-preview.png"
    if social.is_file():
        try:
            width, height = _read_png_dimensions(social)
            if (width, height) != (1280, 640):
                findings.append(
                    _finding(
                        "error",
                        "social-preview-dimensions",
                        "assets/social-preview.png",
                        f"Expected 1280x640; found {width}x{height}.",
                    )
                )
            if social.stat().st_size >= 1_000_000:
                findings.append(
                    _finding(
                        "error",
                        "social-preview-size",
                        "assets/social-preview.png",
                        "GitHub social preview must remain below 1 MB.",
                    )
                )
            chunks = _png_metadata_chunks(social)
            if chunks:
                findings.append(
                    _finding(
                        "warning",
                        "social-preview-metadata",
                        "assets/social-preview.png",
                        f"PNG contains metadata chunks: {', '.join(sorted(chunks))}.",
                        remediation="Strip metadata or verify that every field is intentionally public.",
                    )
                )
        except (OSError, ValueError, struct.error) as exc:
            findings.append(
                _finding("error", "social-preview-invalid", "assets/social-preview.png", str(exc))
            )
    return findings


def check_issue_templates(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    directory = root / ".github/ISSUE_TEMPLATE"
    if not directory.is_dir():
        return findings
    normalized: dict[str, list[str]] = {}
    for path in sorted(directory.glob("*.yml")):
        if path.name == "config.yml":
            continue
        key = re.sub(r"[-_]", "", path.stem).casefold()
        normalized.setdefault(key, []).append(path.name)
    for files in normalized.values():
        if len(files) > 1:
            findings.append(
                _finding(
                    "error",
                    "duplicate-issue-form",
                    ".github/ISSUE_TEMPLATE",
                    f"Issue forms appear to duplicate the same purpose: {', '.join(files)}.",
                    remediation="Keep one canonical form per purpose.",
                )
            )
    config = directory / "config.yml"
    if config.is_file():
        text = config.read_text(encoding="utf-8")
        if re.search(r"url:\s*(?:\.\.?/|/)", text):
            findings.append(
                _finding(
                    "error",
                    "relative-contact-link",
                    ".github/ISSUE_TEMPLATE/config.yml",
                    "GitHub issue-template contact links require an absolute URL.",
                )
            )
    return findings


def check_workflow_paths(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    workflow = root / ".github/workflows/quality.yml"
    if not workflow.is_file():
        return findings
    text = workflow.read_text(encoding="utf-8")
    required_fragments = (
        "scripts/quality/validate_public_repository.py",
        "scripts/quality/audit_publication.py",
        "tests/quality",
        "standard/template/tests/standards",
        "standard/template/scripts/maintenance/validate_repository_standard.py",
    )
    for fragment in required_fragments:
        if fragment not in text:
            findings.append(
                _finding(
                    "error",
                    "workflow-check-missing",
                    ".github/workflows/quality.yml",
                    f"Quality workflow does not reference required check: {fragment}.",
                )
            )
    if "persist-credentials: false" not in text:
        findings.append(
            _finding(
                "warning",
                "checkout-credentials-persist",
                ".github/workflows/quality.yml",
                "Checkout should disable persisted Git credentials for this read-only validation workflow.",
            )
        )
    return findings


def check_agents_budget(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    manifest_path = root / ".repo-standard.json"
    agents_path = root / "AGENTS.md"
    if not manifest_path.is_file() or not agents_path.is_file():
        return findings
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        budget = int(manifest.get("agent_context", {}).get("agents_md_max_bytes", 16_384))
    except (json.JSONDecodeError, TypeError, ValueError):
        return findings
    size = agents_path.stat().st_size
    if size > budget:
        findings.append(
            _finding(
                "error",
                "agents-file-too-large",
                "AGENTS.md",
                f"AGENTS.md is {size} bytes, above the declared {budget}-byte budget.",
                remediation="Move specialized procedures into focused skills or documentation.",
            )
        )
    return findings


def validate(root: Path) -> list[Finding]:
    checks = (
        check_required_files,
        check_generated_files,
        check_identity_and_version,
        check_markdown_links,
        check_machine_readable_files,
        check_assets,
        check_issue_templates,
        check_workflow_paths,
        check_agents_budget,
    )
    findings: list[Finding] = []
    for check in checks:
        findings.extend(check(root))
    return sorted(findings, key=lambda item: (item.severity != "error", item.path, item.line or 0, item.code))


def _print_text(root: Path, findings: Sequence[Finding], strict: bool) -> None:
    counts = {level: sum(item.severity == level for item in findings) for level in ("error", "warning", "info")}
    passed = counts["error"] == 0 and (counts["warning"] == 0 or not strict)
    print(f"Public repository validation: {root}")
    print(f"Errors: {counts['error']}  Warnings: {counts['warning']}  Info: {counts['info']}")
    for item in findings:
        location = item.path + (f":{item.line}" if item.line else "")
        print(f"\n[{item.severity.upper()}] {item.code}: {location}")
        print(f"  {item.message}")
        if item.remediation:
            print(f"  Remediation: {item.remediation}")
    print(f"\nRESULT: {'PASS' if passed else 'FAIL'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to validate.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")
    findings = validate(root)
    counts = {level: sum(item.severity == level for item in findings) for level in ("error", "warning", "info")}
    passed = counts["error"] == 0 and (counts["warning"] == 0 or not args.strict)
    if args.json:
        print(
            json.dumps(
                {
                    "root": str(root),
                    "standard": STANDARD_ID,
                    "passed": passed,
                    "strict": args.strict,
                    "summary": counts,
                    "findings": [asdict(item) for item in findings],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        _print_text(root, findings, args.strict)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())

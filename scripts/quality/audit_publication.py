#!/usr/bin/env python3
"""Audit VCRS files before a public release.

The audit is dependency-free. It checks common disclosure patterns, required
community files, relative links, version consistency, generated artifacts, and
social-preview metadata. It is conservative and cannot replace a full Git
history scan or a dedicated secret scanner.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import struct
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

TEXT_SUFFIXES = {
    "",
    ".cff",
    ".css",
    ".html",
    ".ini",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SKIP_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "coverage",
    "htmlcov",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
}

REQUIRED_PATHS = (
    "README.md",
    "WHITEPAPER.md",
    "AGENTS.md",
    ".repo-standard.json",
    ".codex/config.toml",
    "PUBLISHING.md",
    "LICENSE",
    "NOTICE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "GOVERNANCE.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "THIRD_PARTY_NOTICES.md",
    "ACKNOWLEDGEMENTS.md",
    "VERSION",
    "llms.txt",
    "docs/getting-started.md",
    "docs/faq.md",
    "docs/glossary.md",
    "docs/publication-audit.md",
    "docs/discovery-and-launch.md",
    "assets/vcrs-hero.svg",
    "assets/vcrs-logo.svg",
    "assets/social-preview.png",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/documentation.yml",
    ".github/ISSUE_TEMPLATE/feature.yml",
    ".github/workflows/quality.yml",
    "scripts/quality/audit_publication.py",
    "scripts/quality/validate_public_repository.py",
    "scripts/release/build_release.py",
    "standard/README.md",
    "standard/handbook/README.md",
    "standard/prompts/README.md",
    "standard/handbook/02-canonical-repository-standard.md",
    "standard/template/.repo-standard.json",
    "standard/template/scripts/maintenance/validate_repository_standard.py",
)

FORBIDDEN_FILE_PATTERNS = (
    re.compile(r"(^|/)\.env(?:\..+)?$", re.IGNORECASE),
    re.compile(r"\.(?:log|pyc|pyo|sqlite|sqlite3|db|pem|key|p12|pfx|jks)$", re.IGNORECASE),
    re.compile(r"\.(?:zip|tar|tgz|gz|bz2|xz|7z|rar)$", re.IGNORECASE),
    re.compile(r"(^|/)(?:\.DS_Store|Thumbs\.db)$", re.IGNORECASE),
)

SENSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str], str], ...] = (
    (
        "private-key",
        re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
        "Private-key material must never be published.",
    ),
    (
        "github-token",
        re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})\b"),
        "Possible GitHub access token.",
    ),
    (
        "openai-key",
        re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
        "Possible OpenAI API key.",
    ),
    (
        "aws-access-key",
        re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
        "Possible AWS access-key identifier.",
    ),
    (
        "slack-token",
        re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
        "Possible Slack token.",
    ),
    (
        "google-api-key",
        re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
        "Possible Google API key.",
    ),
    (
        "credential-url",
        re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s/:@]+:[^\s/@]+@", re.IGNORECASE),
        "URL appears to contain embedded credentials.",
    ),
    (
        "personal-email",
        re.compile(r"(?<![\w.+-])[\w.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.-])"),
        "Email address found; confirm that publishing it is intentional.",
    ),
    (
        "unix-home-path",
        re.compile(r"(?<![A-Za-z0-9_])/(?:Users|home)/[A-Za-z0-9._-]+/"),
        "User-specific home-directory path found.",
    ),
    (
        "windows-home-path",
        re.compile(r"(?i)\b[A-Z]:\\Users\\[A-Za-z0-9._ -]+\\"),
        "User-specific Windows home-directory path found.",
    ),
)

GENERIC_SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
    r"connection[_-]?string|password|passwd|private[_-]?key|secret|token)\b"
    r"\s*[:=]\s*(['\"])([^'\"\n]{8,})\1"
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_REFERENCE = re.compile(r"(?:src|href)=[\"']([^\"']+)[\"']", re.IGNORECASE)
PUBLIC_PLACEHOLDER = re.compile(
    r"(?i)(?:\b(?:TODO|TBD|CHANGEME|FIXME)\b|"
    r"<\s*(?:owner|repository|email|url|project-name|replace-me)\s*>)"
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int | None
    message: str


def iter_files(root: Path) -> Iterable[Path]:
    for current, directories, files in os.walk(root):
        directories[:] = sorted(d for d in directories if d not in SKIP_DIRECTORIES)
        base = Path(current)
        for name in sorted(files):
            yield base / name


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES or path.name in {
        "LICENSE",
        "NOTICE",
        "VERSION",
        "llms.txt",
    }


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def looks_like_placeholder(value: str) -> bool:
    normalized = value.strip().lower()
    return (
        normalized.startswith(("<", "${", "{{"))
        or normalized.endswith(">")
        or normalized in {"example", "example-value", "redacted", "replace-me", "changeme"}
        or "example" in normalized
        or "redact" in normalized
        or "placeholder" in normalized
    )


def scan_text(path: Path, text: str, root: Path, deny_terms: Sequence[str]) -> list[Finding]:
    findings: list[Finding] = []
    rel = relative(path, root)

    for code, pattern, message in SENSITIVE_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(Finding("error", code, rel, line_number(text, match.start()), message))

    for match in GENERIC_SECRET_ASSIGNMENT.finditer(text):
        value = match.group(2)
        if not looks_like_placeholder(value):
            findings.append(
                Finding(
                    "error",
                    "secret-assignment",
                    rel,
                    line_number(text, match.start()),
                    "Possible hard-coded secret assignment.",
                )
            )

    lowered = text.casefold()
    for term in deny_terms:
        clean = term.strip()
        if not clean:
            continue
        start = 0
        needle = clean.casefold()
        while True:
            index = lowered.find(needle, start)
            if index < 0:
                break
            findings.append(
                Finding(
                    "error",
                    "private-deny-term",
                    rel,
                    line_number(text, index),
                    "A caller-supplied private or project-specific deny term was found.",
                )
            )
            start = index + len(needle)

    # Public-facing files should not contain unfinished ownership or copy placeholders.
    if rel in {
        "README.md",
        "WHITEPAPER.md",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "SUPPORT.md",
        "GOVERNANCE.md",
    } or rel.startswith("docs/"):
        for match in PUBLIC_PLACEHOLDER.finditer(text):
            findings.append(
                Finding(
                    "error",
                    "public-placeholder",
                    rel,
                    line_number(text, match.start()),
                    "Unresolved placeholder or editorial marker in public-facing content.",
                )
            )

    return findings


def normalize_link_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(")"):
        target = target[1:-1]
    # Markdown permits an optional title after a whitespace separator.
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return target


def check_relative_links(path: Path, text: str, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    rel = relative(path, root)
    candidates: list[tuple[str, int]] = []
    for pattern in (MARKDOWN_LINK, MARKDOWN_IMAGE, HTML_REFERENCE):
        for match in pattern.finditer(text):
            candidates.append((match.group(1), match.start(1)))

    for raw_target, offset in candidates:
        target = normalize_link_target(raw_target)
        if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        destination = (path.parent / target).resolve()
        try:
            destination.relative_to(root.resolve())
        except ValueError:
            findings.append(
                Finding(
                    "error",
                    "link-outside-root",
                    rel,
                    line_number(text, offset),
                    f"Relative link escapes the repository root: {raw_target}",
                )
            )
            continue
        if not destination.exists():
            findings.append(
                Finding(
                    "error",
                    "broken-relative-link",
                    rel,
                    line_number(text, offset),
                    f"Relative link target does not exist: {raw_target}",
                )
            )
    return findings


def read_png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        with path.open("rb") as handle:
            header = handle.read(24)
    except OSError:
        return None
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", header[16:24])


def read_png_metadata_chunks(path: Path) -> set[str]:
    try:
        data = path.read_bytes()
    except OSError:
        return set()
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


def check_required_paths(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for item in REQUIRED_PATHS:
        if not (root / item).exists():
            findings.append(Finding("error", "required-path-missing", item, None, "Required public-release path is missing."))
    return findings


def check_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root):
        rel = relative(path, root)
        for pattern in FORBIDDEN_FILE_PATTERNS:
            if pattern.search(rel):
                findings.append(
                    Finding(
                        "error",
                        "forbidden-artifact",
                        rel,
                        None,
                        "Generated, secret-like, database, key, log, or archive artifact should not be committed.",
                    )
                )
                break
    readme = root / "README.md"
    if readme.is_file() and readme.stat().st_size > 500 * 1024:
        findings.append(
            Finding(
                "error",
                "readme-too-large",
                "README.md",
                None,
                "README exceeds GitHub's 500 KiB rendering threshold.",
            )
        )
    return findings


def check_version_consistency(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    version_path = root / "VERSION"
    try:
        version = version_path.read_text(encoding="utf-8").strip()
    except OSError:
        return findings
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        findings.append(Finding("error", "invalid-version", "VERSION", 1, "VERSION is not a valid semantic version."))
        return findings

    checks = {
        "README.md": (rf"\b{re.escape(version)}\b", "README does not contain the release version."),
        "CHANGELOG.md": (rf"(?:^|\n)##\s+\[?{re.escape(version)}\]?\b", "Changelog has no heading for the release version."),
        "CITATION.cff": (rf"(?m)^version:\s*[\"']?{re.escape(version)}[\"']?\s*$", "CITATION.cff version differs from VERSION."),
        "standard/handbook/02-canonical-repository-standard.md": (
            rf"(?m)^\*\*Version:\*\*\s+{re.escape(version)}\s*$",
            "Normative standard version differs from VERSION.",
        ),
    }
    for rel, (pattern, message) in checks.items():
        path = root / rel
        text = read_text(path) if path.is_file() else None
        if text is not None and re.search(pattern, text) is None:
            findings.append(Finding("error", "version-mismatch", rel, None, message))

    for manifest_relative in (".repo-standard.json", "standard/template/.repo-standard.json"):
        manifest_path = root / manifest_relative
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest_version = manifest["standard"]["version"]
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            findings.append(Finding("error", "manifest-invalid", relative(manifest_path, root), None, "Cannot read standard version from manifest."))
        else:
            if manifest_version != version:
                findings.append(
                    Finding(
                        "error",
                        "version-mismatch",
                        relative(manifest_path, root),
                        None,
                        f"Manifest version {manifest_version!r} differs from VERSION {version!r}.",
                    )
                )
    return findings


def check_structured_files(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in iter_files(root):
        rel = relative(path, root)
        try:
            if path.suffix.lower() == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix.lower() == ".toml":
                with path.open("rb") as handle:
                    tomllib.load(handle)
            elif path.suffix.lower() == ".py":
                compile(path.read_text(encoding="utf-8"), rel, "exec")
        except (OSError, UnicodeError, json.JSONDecodeError, tomllib.TOMLDecodeError, SyntaxError) as exc:
            findings.append(Finding("error", "structured-file-invalid", rel, None, f"Cannot parse file: {exc}"))
    return findings


def check_file_manifest(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    manifest_path = root / "FILE-MANIFEST.sha256"
    if not manifest_path.is_file():
        return findings
    entries: dict[str, str] = {}
    try:
        lines = manifest_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [Finding("error", "manifest-unreadable", "FILE-MANIFEST.sha256", None, str(exc))]
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            findings.append(Finding("error", "manifest-line-invalid", "FILE-MANIFEST.sha256", index, "Invalid SHA-256 manifest line."))
            continue
        entries[match.group(2)] = match.group(1)
    expected = {
        relative(path, root)
        for path in iter_files(root)
        if relative(path, root) != "FILE-MANIFEST.sha256"
    }
    for rel in sorted(expected - entries.keys()):
        findings.append(Finding("error", "manifest-entry-missing", "FILE-MANIFEST.sha256", None, f"Manifest is missing {rel}."))
    for rel in sorted(entries.keys() - expected):
        findings.append(Finding("error", "manifest-entry-extra", "FILE-MANIFEST.sha256", None, f"Manifest references absent file {rel}."))
    import hashlib
    for rel in sorted(expected & entries.keys()):
        actual = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        if actual != entries[rel]:
            findings.append(Finding("error", "manifest-hash-mismatch", rel, None, "File hash differs from FILE-MANIFEST.sha256."))
    return findings


def check_assets(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    preview = root / "assets/social-preview.png"
    if preview.is_file():
        dimensions = read_png_dimensions(preview)
        if dimensions is None:
            findings.append(Finding("error", "social-preview-invalid", relative(preview, root), None, "Social preview is not a valid PNG."))
        elif dimensions != (1280, 640):
            findings.append(
                Finding(
                    "error",
                    "social-preview-size",
                    relative(preview, root),
                    None,
                    f"Social preview is {dimensions[0]}×{dimensions[1]}; expected 1280×640.",
                )
            )
        if preview.stat().st_size >= 1_000_000:
            findings.append(Finding("error", "social-preview-filesize", relative(preview, root), None, "Social preview must be smaller than 1 MB."))
        metadata_chunks = read_png_metadata_chunks(preview)
        if metadata_chunks:
            findings.append(
                Finding(
                    "warning",
                    "social-preview-metadata",
                    relative(preview, root),
                    None,
                    f"Social preview contains metadata chunks: {', '.join(sorted(metadata_chunks))}.",
                )
            )

    hero = root / "assets/vcrs-hero.svg"
    if hero.is_file():
        text = read_text(hero)
        if text is None or "<svg" not in text or "Vibe Coding Repository Standard" not in text:
            findings.append(Finding("error", "hero-invalid", relative(hero, root), None, "Hero SVG is missing expected SVG or project-title content."))
    return findings


def audit(root: Path, deny_terms: Sequence[str] = ()) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    findings.extend(check_required_paths(root))
    findings.extend(check_files(root))
    findings.extend(check_version_consistency(root))
    findings.extend(check_structured_files(root))
    findings.extend(check_file_manifest(root))
    findings.extend(check_assets(root))

    for path in iter_files(root):
        if not is_text_file(path):
            continue
        text = read_text(path)
        if text is None:
            findings.append(Finding("warning", "unreadable-text", relative(path, root), None, "Could not read expected text file as UTF-8."))
            continue
        findings.extend(scan_text(path, text, root, deny_terms))
        if path.suffix.lower() == ".md":
            findings.extend(check_relative_links(path, text, root))

    return sorted(findings, key=lambda item: (item.severity != "error", item.path, item.line or 0, item.code))


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root to audit.")
    parser.add_argument(
        "--deny-term",
        action="append",
        default=[],
        help="Private or project-specific term that must not appear. May be repeated.",
    )
    parser.add_argument(
        "--deny-term-file", "--deny-file",
        dest="deny_term_files",
        action="append",
        type=Path,
        default=[],
        help="External UTF-8 file containing one private deny term per line. Keep it outside the repository. May be repeated.",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as release-blocking findings.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args(argv)


def load_deny_terms(args: argparse.Namespace) -> list[str]:
    terms = list(args.deny_term)
    for deny_file in args.deny_term_files:
        try:
            lines = deny_file.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise SystemExit(f"Cannot read deny file: {exc}") from exc
        terms.extend(line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#"))
    seen: set[str] = set()
    unique: list[str] = []
    for term in terms:
        clean = term.strip()
        key = clean.casefold()
        if clean and key not in seen:
            seen.add(key)
            unique.append(clean)
    return unique


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: repository root does not exist: {root}", file=sys.stderr)
        return 2

    findings = audit(root, load_deny_terms(args))
    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]

    if args.json:
        print(json.dumps({"root": str(root), "findings": [asdict(item) for item in findings]}, indent=2))
    else:
        for item in findings:
            location = item.path + (f":{item.line}" if item.line else "")
            print(f"{item.severity.upper():7} {item.code:28} {location} — {item.message}")
        print(f"Publication audit: {len(errors)} error(s), {len(warnings)} warning(s).")
        if not findings:
            print("No findings. This is not a substitute for a full Git-history and dedicated secret scan.")

    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())

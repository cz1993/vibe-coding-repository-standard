#!/usr/bin/env python3
"""Build a deterministic VCRS source-release ZIP with a SHA-256 manifest.

By default the script validates the public repository and runs the publication
audit before packaging. It excludes Git metadata, caches, local audit inputs,
and generated output. The release archive contains one top-level directory.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

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
    ".audit-private",
}

SKIP_FILENAMES = {
    ".DS_Store",
    "Thumbs.db",
    "FILE-MANIFEST.sha256",
}

SKIP_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
    ".swp",
    ".zip",
}

ZIP_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


@dataclass(frozen=True)
class ReleaseResult:
    archive: str
    checksum_file: str
    sha256: str
    version: str
    files: int
    bytes: int


def _iter_release_files(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = sorted(name for name in dirs if name not in SKIP_DIRS)
        base = Path(current)
        for name in sorted(files):
            path = base / name
            if name in SKIP_FILENAMES or path.suffix.lower() in SKIP_SUFFIXES:
                continue
            yield path


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest(files: Sequence[tuple[str, bytes]]) -> bytes:
    lines = [f"{_sha256_bytes(data)}  {relative}" for relative, data in files]
    return ("\n".join(lines) + "\n").encode("utf-8")


def _zip_entry(name: str, data: bytes, executable: bool) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    mode = 0o755 if executable else 0o644
    info.external_attr = (mode & 0xFFFF) << 16
    return info, data


def build_archive(root: Path, output_dir: Path, project_slug: str, version: str) -> ReleaseResult:
    root = root.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_name = f"{project_slug}-v{version}.zip"
    archive_path = output_dir / archive_name
    checksum_path = output_dir / f"{archive_name}.sha256"
    top = f"{project_slug}-{version}"

    collected: list[tuple[str, bytes, bool]] = []
    for path in _iter_release_files(root):
        relative = path.relative_to(root).as_posix()
        data = path.read_bytes()
        executable = bool(path.stat().st_mode & 0o111)
        collected.append((relative, data, executable))
    collected.sort(key=lambda item: item[0])

    manifest_data = _manifest([(relative, data) for relative, data, _ in collected])
    collected.append(("FILE-MANIFEST.sha256", manifest_data, False))

    with tempfile.NamedTemporaryFile(dir=output_dir, prefix=f".{archive_name}.", delete=False) as temp:
        temp_path = Path(temp.name)
    try:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for relative, data, executable in collected:
                info, payload = _zip_entry(f"{top}/{relative}", data, executable)
                archive.writestr(info, payload)
        temp_path.replace(archive_path)
        archive_path.chmod(0o644)
    finally:
        temp_path.unlink(missing_ok=True)

    digest = _sha256_file(archive_path)
    checksum_path.write_text(f"{digest}  {archive_name}\n", encoding="utf-8")
    return ReleaseResult(
        archive=str(archive_path),
        checksum_file=str(checksum_path),
        sha256=digest,
        version=version,
        files=len(collected),
        bytes=archive_path.stat().st_size,
    )


def _run(command: Sequence[str], cwd: Path) -> None:
    # Validation diagnostics go to stderr so --json keeps stdout machine-readable.
    print("+ " + " ".join(command), file=sys.stderr)
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        stdout=sys.stderr,
        stderr=sys.stderr,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def _read_version(root: Path) -> str:
    path = root / "VERSION"
    if not path.is_file():
        raise SystemExit(f"Missing VERSION file: {path}")
    version = path.read_text(encoding="utf-8").strip()
    if not version:
        raise SystemExit("VERSION is empty")
    return version


def validate_before_build(root: Path, deny_terms: Sequence[str], deny_term_files: Sequence[Path]) -> None:
    python = sys.executable
    _run([python, "scripts/quality/validate_public_repository.py", "--root", ".", "--strict"], root)
    audit = [python, "scripts/quality/audit_publication.py", "--root", ".", "--strict"]
    for term in deny_terms:
        audit.extend(["--deny-term", term])
    for path in deny_term_files:
        audit.extend(["--deny-file", str(path.expanduser().resolve())])
    _run(audit, root)
    _run([python, "-m", "unittest", "discover", "-s", "tests/quality", "-p", "test_*.py", "-v"], root)
    _run(
        [python, "-m", "unittest", "discover", "-s", "standard/template/tests/standards", "-p", "test_*.py", "-v"],
        root,
    )
    _run(
        [python, "standard/template/scripts/maintenance/validate_repository_standard.py", "--root", "standard/template"],
        root,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Public repository root.")
    parser.add_argument("--output-dir", type=Path, default=Path("dist"), help="Destination directory.")
    parser.add_argument("--project-slug", default="vibe-coding-repository-standard")
    parser.add_argument("--version", help="Override VERSION for a controlled test build.")
    parser.add_argument("--deny-term", action="append", default=[], help="Private term that must not appear.")
    parser.add_argument(
        "--deny-term-file",
        action="append",
        type=Path,
        default=[],
        help="Private deny-term file stored outside the repository.",
    )
    parser.add_argument("--skip-validation", action="store_true", help="Package without validation; intended for tests only.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable result JSON.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")
    output_dir = args.output_dir.expanduser()
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    version = args.version or _read_version(root)
    if not args.skip_validation:
        validate_before_build(root, args.deny_term, args.deny_term_file)
    result = build_archive(root, output_dir, args.project_slug, version)
    if args.json:
        print(json.dumps(asdict(result), indent=2, sort_keys=True))
    else:
        print(f"Release archive: {result.archive}")
        print(f"SHA-256: {result.sha256}")
        print(f"Checksum file: {result.checksum_file}")
        print(f"Files: {result.files}  Bytes: {result.bytes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

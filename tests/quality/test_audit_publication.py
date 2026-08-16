from __future__ import annotations

import importlib.util
import struct
import sys
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[2] / "scripts" / "quality" / "audit_publication.py"
SPEC = importlib.util.spec_from_file_location("audit_publication", MODULE_PATH)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


def write_png(path: Path, width: int, height: int) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + b"\x00\x00\x00" * width for _ in range(height))
    payload = b"\x89PNG\r\n\x1a\n"
    payload += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    payload += chunk(b"IDAT", zlib.compress(raw))
    payload += chunk(b"IEND", b"")
    path.write_bytes(payload)


class PublicationAuditTests(unittest.TestCase):
    def test_detects_common_secret_patterns(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "example.md"
            text = ("pass" + "word = \"correct-horse-battery-staple\"\n" + "-----BEGIN " + "PRIVATE KEY-----\n")
            findings = AUDIT.scan_text(path, text, root, [])
            codes = {item.code for item in findings}
            self.assertIn("secret-assignment", codes)
            self.assertIn("private-key", codes)

    def test_allows_explicit_placeholder_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "example.md"
            findings = AUDIT.scan_text(path, 'api_key = "<replace-me>"\n', root, [])
            self.assertNotIn("secret-assignment", {item.code for item in findings})

    def test_detects_private_deny_term_case_insensitively(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "example.md"
            findings = AUDIT.scan_text(path, "PrivateProject is mentioned here.", root, ["privateproject"])
            self.assertIn("private-deny-term", {item.code for item in findings})

    def test_detects_broken_relative_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "README.md"
            path.write_text("[Missing](docs/missing.md)\n", encoding="utf-8")
            findings = AUDIT.check_relative_links(path, path.read_text(encoding="utf-8"), root)
            self.assertIn("broken-relative-link", {item.code for item in findings})

    def test_accepts_existing_relative_link(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            docs = root / "docs"
            docs.mkdir()
            target = docs / "guide.md"
            target.write_text("# Guide\n", encoding="utf-8")
            path = root / "README.md"
            path.write_text("[Guide](docs/guide.md)\n", encoding="utf-8")
            self.assertEqual([], AUDIT.check_relative_links(path, path.read_text(encoding="utf-8"), root))

    def test_reads_png_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preview.png"
            write_png(path, 1280, 640)
            self.assertEqual((1280, 640), AUDIT.read_png_dimensions(path))

    def test_detects_version_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "standard/template").mkdir(parents=True)
            (root / "standard/handbook").mkdir(parents=True)
            (root / "VERSION").write_text("1.2.3\n", encoding="utf-8")
            (root / "README.md").write_text("Version 1.2.3\n", encoding="utf-8")
            (root / "CHANGELOG.md").write_text("## 1.2.3\n", encoding="utf-8")
            (root / "CITATION.cff").write_text("version: 1.2.3\n", encoding="utf-8")
            (root / "standard/handbook/02-canonical-repository-standard.md").write_text(
                "**Version:** 1.2.3\n", encoding="utf-8"
            )
            (root / "standard/template/.repo-standard.json").write_text(
                '{"standard": {"version": "9.9.9"}}', encoding="utf-8"
            )
            findings = AUDIT.check_version_consistency(root)
            self.assertIn("version-mismatch", {item.code for item in findings})


if __name__ == "__main__":
    unittest.main()

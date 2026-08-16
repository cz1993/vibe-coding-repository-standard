from __future__ import annotations

import importlib.util
import json
import struct
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "scripts" / "quality" / "validate_public_repository.py"
SPEC = importlib.util.spec_from_file_location("validate_public_repository", MODULE_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def make_png(width: int, height: int) -> bytes:
    signature = b"\x89PNG\r\n\x1a\n"

    def chunk(kind: bytes, data: bytes) -> bytes:
        payload = kind + data
        return struct.pack(">I", len(data)) + payload + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return signature + chunk(b"IHDR", ihdr) + chunk(b"IEND", b"")


class PublicRepositoryValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, content: str | bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def codes(self, findings):
        return {item.code for item in findings}

    def test_broken_relative_link_is_error(self) -> None:
        self.write("README.md", "See [missing](docs/missing.md).\n")
        findings = VALIDATOR.check_markdown_links(self.root)
        self.assertIn("broken-relative-link", self.codes(findings))

    def test_link_outside_repository_is_error(self) -> None:
        self.write("README.md", "See [outside](../../private.txt).\n")
        findings = VALIDATOR.check_markdown_links(self.root)
        self.assertIn("link-escapes-repository", self.codes(findings))

    def test_generated_archive_is_error(self) -> None:
        self.write("release.zip", b"not an archive")
        findings = VALIDATOR.check_generated_files(self.root)
        self.assertIn("generated-or-private-file", self.codes(findings))

    def test_invalid_json_is_error(self) -> None:
        self.write("broken.json", "{not-json}\n")
        findings = VALIDATOR.check_machine_readable_files(self.root)
        self.assertIn("machine-readable-parse-error", self.codes(findings))

    def test_duplicate_issue_form_names_are_error(self) -> None:
        form = "name: Example\ndescription: Example\nbody: []\n"
        self.write(".github/ISSUE_TEMPLATE/bug-report.yml", form)
        self.write(".github/ISSUE_TEMPLATE/bug_report.yml", form)
        findings = VALIDATOR.check_issue_templates(self.root)
        self.assertIn("duplicate-issue-form", self.codes(findings))

    def test_wrong_social_preview_dimensions_are_error(self) -> None:
        self.write("assets/social-preview.png", make_png(640, 320))
        findings = VALIDATOR.check_assets(self.root)
        self.assertIn("social-preview-dimensions", self.codes(findings))

    def test_current_repository_passes_strict(self) -> None:
        repository_root = Path(__file__).parents[2]
        findings = VALIDATOR.validate(repository_root)
        blocking = [item for item in findings if item.severity in {"error", "warning"}]
        self.assertEqual([], blocking, "\n".join(f"{item.code}: {item.path}: {item.message}" for item in blocking))


if __name__ == "__main__":
    unittest.main()

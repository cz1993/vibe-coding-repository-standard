from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "scripts" / "release" / "build_release.py"
SPEC = importlib.util.spec_from_file_location("build_release", MODULE_PATH)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BUILDER
SPEC.loader.exec_module(BUILDER)


class ReleaseBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.output = self.base / "output"
        self.root.mkdir()
        (self.root / "README.md").write_text("# Example\n", encoding="utf-8")
        (self.root / "VERSION").write_text("0.1.0\n", encoding="utf-8")
        (self.root / "scripts").mkdir()
        script = self.root / "scripts" / "run.py"
        script.write_text("print('ok')\n", encoding="utf-8")
        script.chmod(0o755)
        (self.root / "__pycache__").mkdir()
        (self.root / "__pycache__" / "ignored.pyc").write_bytes(b"cache")
        (self.root / ".git").mkdir()
        (self.root / ".git" / "config").write_text("private history metadata", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_archive_contains_manifest_and_excludes_private_outputs(self) -> None:
        result = BUILDER.build_archive(self.root, self.output, "example", "0.1.0")
        archive = Path(result.archive)
        self.assertTrue(archive.is_file())
        with zipfile.ZipFile(archive) as handle:
            names = set(handle.namelist())
            self.assertIn("example-0.1.0/README.md", names)
            self.assertIn("example-0.1.0/FILE-MANIFEST.sha256", names)
            self.assertNotIn("example-0.1.0/.git/config", names)
            self.assertNotIn("example-0.1.0/__pycache__/ignored.pyc", names)

    def test_build_is_deterministic_for_unchanged_input(self) -> None:
        first = BUILDER.build_archive(self.root, self.output / "one", "example", "0.1.0")
        second = BUILDER.build_archive(self.root, self.output / "two", "example", "0.1.0")
        self.assertEqual(first.sha256, second.sha256)


if __name__ == "__main__":
    unittest.main()

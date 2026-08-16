from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import sys
from pathlib import Path
from unittest import mock

VALIDATOR_PATH = Path(__file__).resolve().parents[2] / "scripts" / "maintenance" / "validate_repository_standard.py"
SPEC = importlib.util.spec_from_file_location("repo_standard_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self._make_compliant_repo()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, content: str = "x\n") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def _make_compliant_repo(self) -> None:
        manifest = {
            "schema_version": 1,
            "standard": {"id": "VCRS-1", "version": "1.0.0"},
            "repository": {
                "name": "fixture-repository",
                "primary_profile": "single-application",
                "secondary_profiles": [],
                "risk_class": "low",
                "governance_owner": "platform-team",
                "last_reviewed": "2026-08-15",
            },
            "agent_context": {
                "agents_md_max_bytes": 16384,
                "allowed_nested_instruction_files": [],
                "allowed_legacy_instruction_files": [],
            },
            "skills": {"active": ["repository-bootstrap", "safe-change", "repository-hygiene"]},
            "optional_capabilities": {"mcp_servers": [], "memory_enabled": False, "hooks_enabled": False},
            "path_exceptions": [],
            "exceptions": [],
        }
        self.write(".repo-standard.json", json.dumps(manifest))
        self.write("README.md", "# Fixture\n")
        self.write("AGENTS.md", "# Instructions\n")
        self.write("scripts/README.md", "# Scripts\n")
        self.write("scripts/maintenance/validate_repository_standard.py", "# fixture\n")
        self.write("tests/standards/test_fixture.py", "# fixture\n")
        for directory in ("docs/architecture", "docs/decisions", "docs/runbooks", "docs/reference"):
            (self.root / directory).mkdir(parents=True, exist_ok=True)
        self.write(
            "docs/README.md",
            "# Docs\n\nStatus: Authoritative\nOwner: team\nLast validated: 2026-08-15\nValidated by: tests\n",
        )
        self.write(
            ".codex/config.toml",
            '''approval_policy = "on-request"\n'''
            '''sandbox_mode = "workspace-write"\n'''
            '''project_doc_max_bytes = 16384\n'''
            '''project_doc_fallback_filenames = []\n'''
            '''[sandbox_workspace_write]\nnetwork_access = false\n'''
            '''[features]\nmemories = false\nhooks = false\nmulti_agent = true\n'''
            '''[agents]\nenabled = true\nmax_concurrent_threads_per_session = 3\ninterrupt_message = true\n'''
            '''[shell_environment_policy]\nignore_default_excludes = false\n''',
        )
        agents = {
            "repo-explorer.toml": ("repo_explorer", "read-only"),
            "executor.toml": ("executor", "workspace-write"),
            "reviewer.toml": ("reviewer", "read-only"),
        }
        for filename, (name, sandbox) in agents.items():
            self.write(
                f".codex/agents/{filename}",
                f'name = "{name}"\ndescription = "fixture role"\nsandbox_mode = "{sandbox}"\ndeveloper_instructions = "fixture"\n',
            )
        descriptions = {
            "repository-bootstrap": "Use only for explicit repository bootstrap; do not use for features.",
            "safe-change": "Use for one bounded change only; do not use for broad cleanup.",
            "repository-hygiene": "Use only for explicit read-only hygiene audits; do not delete.",
        }
        for name, description in descriptions.items():
            self.write(
                f".agents/skills/{name}/SKILL.md",
                f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n",
            )
        self.write(
            ".github/PULL_REQUEST_TEMPLATE.md",
            "# Plain-language summary\n# Scope and non-goals\n# Test evidence\nExpected Actual Evidence\n# Risk and rollback\n# Documentation and agent governance\n",
        )
        self.write(".github/workflows/repository-standard.yml", "name: fixture\n")

    def findings(self):
        return validator.validate_repository(self.root)

    def test_compliant_fixture_has_no_errors(self) -> None:
        errors = [item for item in self.findings() if item.severity == "error"]
        self.assertEqual([], errors)

    def test_oversized_agents_file_is_error(self) -> None:
        self.write("AGENTS.md", "x" * 17000)
        codes = {item.code for item in self.findings() if item.severity == "error"}
        self.assertIn("agents-md-over-budget", codes)

    def test_unknown_nested_instruction_is_warning_and_strict_fails(self) -> None:
        self.write("src/AGENTS.md", "# unexpected\n")
        findings = self.findings()
        self.assertIn("nested-instruction-not-allowlisted", {item.code for item in findings})
        self.assertEqual(0, validator.main(["--root", str(self.root)]))
        self.assertEqual(1, validator.main(["--root", str(self.root), "--strict"]))

    def test_duplicate_skill_name_is_error(self) -> None:
        self.write(
            ".agents/skills/duplicate/SKILL.md",
            "---\nname: safe-change\ndescription: Use only for a duplicate test; do not use normally.\n---\n",
        )
        codes = {item.code for item in self.findings() if item.severity == "error"}
        self.assertIn("duplicate-skill-name", codes)

    def test_network_and_hooks_are_errors(self) -> None:
        config = (self.root / ".codex/config.toml").read_text(encoding="utf-8")
        config = config.replace("network_access = false", "network_access = true")
        config = config.replace("hooks = false", "hooks = true")
        self.write(".codex/config.toml", config)
        codes = {item.code for item in self.findings() if item.severity == "error"}
        self.assertIn("codex-network-enabled", codes)
        self.assertIn("codex-feature-hooks", codes)

    def test_tracked_secret_like_files_are_reported(self) -> None:
        with mock.patch.object(validator, "_tracked_files", return_value=[".env", "keys/client.key", "run.log"]):
            findings = validator.validate_repository(self.root)
        codes = {item.code for item in findings}
        self.assertIn("tracked-env-file", codes)
        self.assertIn("tracked-private-key", codes)
        self.assertIn("tracked-log", codes)

    def test_json_mode_returns_machine_readable_output_status(self) -> None:
        self.assertEqual(0, validator.main(["--root", str(self.root), "--json"]))


if __name__ == "__main__":
    unittest.main()

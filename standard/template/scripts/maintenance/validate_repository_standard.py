#!/usr/bin/env python3
"""Validate the objective parts of the Canonical Repository Standard (VCRS-1).

The validator is intentionally dependency-free. It checks the repository
operating surface; it does not claim that application behavior or architecture
is correct.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

try:
    import tomllib
except ModuleNotFoundError as exc:  # pragma: no cover - Python < 3.11
    raise SystemExit("Python 3.11 or newer is required (tomllib is unavailable).") from exc

STANDARD_ID = "VCRS-1"
VALID_PROFILES = {"single-application", "monorepo", "data-platform", "infrastructure"}

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    ".repo-standard.json",
    ".codex/config.toml",
    ".codex/agents/repo-explorer.toml",
    ".codex/agents/executor.toml",
    ".codex/agents/reviewer.toml",
    ".agents/skills/repository-bootstrap/SKILL.md",
    ".agents/skills/safe-change/SKILL.md",
    ".agents/skills/repository-hygiene/SKILL.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/repository-standard.yml",
    "docs/README.md",
    "scripts/README.md",
    "scripts/maintenance/validate_repository_standard.py",
)

REQUIRED_DIRECTORIES = (
    "docs/architecture",
    "docs/decisions",
    "docs/runbooks",
    "docs/reference",
    "tests/standards",
)

SKIP_DIRS = {
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
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "__pycache__",
}

LEGACY_AGENT_NAMES = {
    "agent.md",
    "memory.md",
    "project-memory.md",
    "agent-context.md",
    "instructions-old.md",
    "agent-instructions-old.md",
}

DOC_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
ADR_NAME_RE = re.compile(r"^[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


@dataclass(frozen=True)
class Finding:
    severity: str  # error | warning | info
    code: str
    path: str
    message: str
    remediation: str = ""


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _iter_files(root: Path, names: set[str] | None = None) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        base = Path(current)
        for filename in files:
            if names is None or filename in names:
                yield base / filename


def _load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, "file does not exist"
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
    if not isinstance(value, dict):
        return None, "top-level JSON value must be an object"
    return value, None


def _load_toml(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        with path.open("rb") as handle:
            value = tomllib.load(handle)
    except FileNotFoundError:
        return None, "file does not exist"
    except (OSError, tomllib.TOMLDecodeError) as exc:
        return None, str(exc)
    return value, None


def _nested(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _parse_skill_frontmatter(path: Path) -> tuple[dict[str, str], str | None]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return {}, str(exc)

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "SKILL.md must begin with YAML front matter delimited by ---"

    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, "SKILL.md front matter has no closing ---"

    metadata: dict[str, str] = {}
    for raw in lines[1:closing]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")):
            # This validator intentionally supports scalar top-level metadata only.
            continue
        key, separator, value = raw.partition(":")
        if separator:
            metadata[key.strip()] = value.strip().strip("'\"")
    return metadata, None


def _tracked_files(root: Path) -> list[str]:
    if not (root / ".git").exists():
        return []
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return [item.decode("utf-8", errors="replace") for item in result.stdout.split(b"\0") if item]


def _check_required(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel_path in REQUIRED_FILES:
        path = root / rel_path
        if not path.is_file():
            findings.append(
                Finding(
                    "error",
                    "required-file-missing",
                    rel_path,
                    "Required repository-standard file is missing.",
                    "Add or map an equivalent through the bootstrap process; do not create an empty placeholder that is never adapted.",
                )
            )
    for rel_path in REQUIRED_DIRECTORIES:
        path = root / rel_path
        if not path.is_dir():
            findings.append(
                Finding(
                    "error",
                    "required-directory-missing",
                    rel_path,
                    "Required repository-standard directory is missing.",
                    "Create the directory or document an approved equivalent path exception.",
                )
            )
    tests_dir = root / "tests/standards"
    if tests_dir.is_dir() and not any(tests_dir.glob("test_*.py")):
        findings.append(
            Finding(
                "error",
                "validator-tests-missing",
                "tests/standards",
                "No test_*.py file exists for the repository-standard validator.",
                "Add dependency-free unit tests for compliant, warning, and failing repositories.",
            )
        )
    return findings


def _check_manifest(root: Path) -> tuple[list[Finding], dict[str, Any]]:
    path = root / ".repo-standard.json"
    manifest, error = _load_json(path)
    if error or manifest is None:
        return [Finding("error", "manifest-invalid", ".repo-standard.json", f"Cannot parse manifest: {error}")], {}

    findings: list[Finding] = []
    if manifest.get("schema_version") != 1:
        findings.append(Finding("error", "manifest-schema", ".repo-standard.json", "schema_version must be 1."))

    standard_id = _nested(manifest, "standard", "id")
    if standard_id != STANDARD_ID:
        findings.append(
            Finding("error", "manifest-standard-id", ".repo-standard.json", f"standard.id must be {STANDARD_ID!r}.")
        )
    version = _nested(manifest, "standard", "version")
    if not isinstance(version, str) or not version.strip():
        findings.append(Finding("error", "manifest-version", ".repo-standard.json", "standard.version is required."))

    profile = _nested(manifest, "repository", "primary_profile")
    if profile not in VALID_PROFILES:
        findings.append(
            Finding(
                "error",
                "manifest-profile",
                ".repo-standard.json",
                f"repository.primary_profile must be one of {sorted(VALID_PROFILES)}.",
            )
        )

    owner = _nested(manifest, "repository", "governance_owner")
    if not isinstance(owner, str) or not owner.strip():
        findings.append(Finding("error", "manifest-owner", ".repo-standard.json", "A governance owner is required."))
    elif owner in {"repository-owner", "replace", "todo", "tbd"}:
        findings.append(
            Finding(
                "warning",
                "manifest-owner-placeholder",
                ".repo-standard.json",
                "The governance owner still appears to be a template placeholder.",
                "Replace it with an accountable person, role, or team before managed adoption.",
            )
        )

    budget = _nested(manifest, "agent_context", "agents_md_max_bytes")
    if not isinstance(budget, int) or isinstance(budget, bool) or budget <= 0:
        findings.append(
            Finding("error", "manifest-agent-budget", ".repo-standard.json", "agents_md_max_bytes must be a positive integer.")
        )

    for key in ("allowed_nested_instruction_files", "allowed_legacy_instruction_files"):
        value = _nested(manifest, "agent_context", key, default=[])
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            findings.append(
                Finding("error", "manifest-list", ".repo-standard.json", f"agent_context.{key} must be an array of paths.")
            )

    active = _nested(manifest, "skills", "active", default=[])
    if not isinstance(active, list) or not all(isinstance(item, str) and item for item in active):
        findings.append(Finding("error", "manifest-skills", ".repo-standard.json", "skills.active must be an array of names."))

    optional = _nested(manifest, "optional_capabilities", default={})
    if not isinstance(optional, dict):
        findings.append(
            Finding("error", "manifest-optional-capabilities", ".repo-standard.json", "optional_capabilities must be an object.")
        )
    else:
        for key in ("memory_enabled", "hooks_enabled"):
            if not isinstance(optional.get(key), bool):
                findings.append(
                    Finding("error", "manifest-optional-boolean", ".repo-standard.json", f"optional_capabilities.{key} must be boolean.")
                )
        if not isinstance(optional.get("mcp_servers", []), list):
            findings.append(
                Finding("error", "manifest-mcp-list", ".repo-standard.json", "optional_capabilities.mcp_servers must be an array.")
            )

    for list_key in ("path_exceptions", "exceptions"):
        if not isinstance(manifest.get(list_key, []), list):
            findings.append(Finding("error", "manifest-exceptions", ".repo-standard.json", f"{list_key} must be an array."))

    repo_name = _nested(manifest, "repository", "name")
    if repo_name in {"repository-name", "replace", "todo", "tbd", None, ""}:
        findings.append(
            Finding(
                "warning",
                "manifest-name-placeholder",
                ".repo-standard.json",
                "The repository name appears to be a template placeholder.",
                "Set repository.name to the actual repository name.",
            )
        )
    return findings, manifest


def _check_agents_md(root: Path, manifest: dict[str, Any]) -> list[Finding]:
    path = root / "AGENTS.md"
    if not path.is_file():
        return []
    budget = _nested(manifest, "agent_context", "agents_md_max_bytes", default=16384)
    if not isinstance(budget, int) or budget <= 0:
        budget = 16384
    size = path.stat().st_size
    findings: list[Finding] = []
    if size > budget:
        findings.append(
            Finding(
                "error",
                "agents-md-over-budget",
                "AGENTS.md",
                f"AGENTS.md is {size} bytes; the manifest budget is {budget} bytes.",
                "Delete duplication/task history, move focused detail to docs or skills, or approve a time-bounded exception.",
            )
        )
    elif size > 8192:
        findings.append(
            Finding(
                "warning",
                "agents-md-above-target",
                "AGENTS.md",
                f"AGENTS.md is {size} bytes, above the recommended 4–8 KiB target.",
                "Review whether focused material can move to skills or authoritative documentation.",
            )
        )
    return findings


def _check_instruction_files(root: Path, manifest: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    allowed_nested = {
        Path(item).as_posix().lstrip("./")
        for item in _nested(manifest, "agent_context", "allowed_nested_instruction_files", default=[])
        if isinstance(item, str)
    }
    allowed_legacy = {
        Path(item).as_posix().lstrip("./")
        for item in _nested(manifest, "agent_context", "allowed_legacy_instruction_files", default=[])
        if isinstance(item, str)
    }

    for path in _iter_files(root, {"AGENTS.md", "AGENTS.override.md"}):
        rel_path = _rel(path, root)
        if rel_path == "AGENTS.md":
            continue
        if rel_path not in allowed_nested:
            findings.append(
                Finding(
                    "warning",
                    "nested-instruction-not-allowlisted",
                    rel_path,
                    "Nested Codex instruction file is not declared in the manifest.",
                    "Remove it, narrow and allowlist it with an owner/scope, or reconcile it into the root instructions.",
                )
            )

    for path in _iter_files(root):
        rel_path = _rel(path, root)
        if path.name.lower() in LEGACY_AGENT_NAMES and rel_path not in allowed_legacy:
            findings.append(
                Finding(
                    "warning",
                    "legacy-agent-surface",
                    rel_path,
                    "Potential legacy agent instruction or memory file may pollute repository search/context.",
                    "Reconcile unique current requirements, then delete or explicitly allowlist a thin compatibility adapter.",
                )
            )
    return findings


def _check_skills(root: Path, manifest: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    skills_root = root / ".agents" / "skills"
    names: dict[str, str] = {}
    if not skills_root.is_dir():
        return findings

    for path in sorted(skills_root.rglob("SKILL.md")):
        metadata, error = _parse_skill_frontmatter(path)
        rel_path = _rel(path, root)
        if error:
            findings.append(Finding("error", "skill-frontmatter", rel_path, error))
            continue
        name = metadata.get("name", "").strip()
        description = metadata.get("description", "").strip()
        if not name:
            findings.append(Finding("error", "skill-name", rel_path, "Skill front matter is missing name."))
        elif name in names:
            findings.append(
                Finding(
                    "error",
                    "duplicate-skill-name",
                    rel_path,
                    f"Skill name {name!r} duplicates {names[name]}.",
                    "Use one unique workflow name; Codex does not merge duplicate skills.",
                )
            )
        else:
            names[name] = rel_path
            if path.parent.name != name:
                findings.append(
                    Finding(
                        "warning",
                        "skill-folder-name",
                        rel_path,
                        f"Skill folder {path.parent.name!r} does not match metadata name {name!r}.",
                        "Align folder and skill names to simplify discovery.",
                    )
                )
        if not description:
            findings.append(Finding("error", "skill-description", rel_path, "Skill front matter is missing description."))
        elif len(description) > 500:
            findings.append(
                Finding(
                    "warning",
                    "skill-description-long",
                    rel_path,
                    f"Skill description is {len(description)} characters.",
                    "Front-load scope and trigger words and keep discovery metadata concise.",
                )
            )
        if description and "do not" not in description.lower() and "only" not in description.lower():
            findings.append(
                Finding(
                    "warning",
                    "skill-trigger-boundary",
                    rel_path,
                    "Skill description does not state an obvious non-trigger or boundary.",
                    "Explain when the skill should and should not activate.",
                )
            )

    active = _nested(manifest, "skills", "active", default=[])
    if isinstance(active, list):
        for name in active:
            if isinstance(name, str) and name not in names:
                findings.append(
                    Finding(
                        "error",
                        "active-skill-missing",
                        ".repo-standard.json",
                        f"Manifest lists active skill {name!r}, but no matching SKILL.md was found.",
                    )
                )
    return findings


def _check_codex_config(root: Path, manifest: dict[str, Any]) -> list[Finding]:
    path = root / ".codex" / "config.toml"
    config, error = _load_toml(path)
    if error or config is None:
        return [Finding("error", "codex-config-invalid", ".codex/config.toml", f"Cannot parse Codex config: {error}")]

    findings: list[Finding] = []
    approval = config.get("approval_policy")
    if approval != "on-request":
        findings.append(
            Finding(
                "warning",
                "codex-approval-policy",
                ".codex/config.toml",
                f"approval_policy is {approval!r}; the baseline expects 'on-request'.",
                "Document why a different interactive approval policy is safe for this repository.",
            )
        )

    sandbox = config.get("sandbox_mode")
    if sandbox == "danger-full-access":
        findings.append(
            Finding(
                "error",
                "codex-dangerous-sandbox",
                ".codex/config.toml",
                "sandbox_mode grants danger-full-access.",
                "Use workspace-write or read-only and request narrow escalation when genuinely required.",
            )
        )
    elif sandbox not in {"workspace-write", "read-only"}:
        findings.append(
            Finding(
                "warning",
                "codex-sandbox-mode",
                ".codex/config.toml",
                f"Unexpected sandbox_mode {sandbox!r}.",
                "Use workspace-write for normal development or read-only for audit/review.",
            )
        )

    network = _nested(config, "sandbox_workspace_write", "network_access", default=False)
    if network is not False:
        findings.append(
            Finding(
                "error",
                "codex-network-enabled",
                ".codex/config.toml",
                "Workspace sandbox outbound network is enabled in the baseline config.",
                "Disable it and admit network access separately for bounded workflows.",
            )
        )

    fallbacks = config.get("project_doc_fallback_filenames", [])
    if fallbacks not in ([], None):
        findings.append(
            Finding(
                "warning",
                "codex-agent-fallbacks",
                ".codex/config.toml",
                "Additional project instruction fallback filenames are configured.",
                "Prefer canonical AGENTS.md and remove aliases unless a documented compatibility requirement exists.",
            )
        )

    configured_budget = config.get("project_doc_max_bytes")
    manifest_budget = _nested(manifest, "agent_context", "agents_md_max_bytes", default=16384)
    if not isinstance(configured_budget, int) or configured_budget <= 0:
        findings.append(
            Finding("error", "codex-doc-budget", ".codex/config.toml", "project_doc_max_bytes must be a positive integer.")
        )
    elif isinstance(manifest_budget, int) and configured_budget != manifest_budget:
        findings.append(
            Finding(
                "warning",
                "codex-budget-mismatch",
                ".codex/config.toml",
                f"project_doc_max_bytes ({configured_budget}) differs from manifest budget ({manifest_budget}).",
                "Use one approved budget or record an explicit exception.",
            )
        )

    for feature, expected, severity in (
        ("memories", False, "error"),
        ("hooks", False, "error"),
        ("multi_agent", True, "warning"),
    ):
        actual = _nested(config, "features", feature)
        if actual is not expected:
            findings.append(
                Finding(
                    severity,
                    f"codex-feature-{feature}",
                    ".codex/config.toml",
                    f"features.{feature} is {actual!r}; baseline expects {expected!r}.",
                    "Use the baseline setting or record and review a project-specific capability admission.",
                )
            )

    manifest_optional = _nested(manifest, "optional_capabilities", default={})
    if isinstance(manifest_optional, dict):
        if manifest_optional.get("memory_enabled") != _nested(config, "features", "memories"):
            findings.append(
                Finding(
                    "warning",
                    "memory-manifest-mismatch",
                    ".repo-standard.json",
                    "Manifest memory_enabled does not match Codex features.memories.",
                )
            )
        if manifest_optional.get("hooks_enabled") != _nested(config, "features", "hooks"):
            findings.append(
                Finding(
                    "warning",
                    "hooks-manifest-mismatch",
                    ".repo-standard.json",
                    "Manifest hooks_enabled does not match Codex features.hooks.",
                )
            )

    concurrent = _nested(config, "agents", "max_concurrent_threads_per_session")
    if not isinstance(concurrent, int) or concurrent <= 0:
        findings.append(
            Finding(
                "error",
                "codex-agent-concurrency",
                ".codex/config.toml",
                "agents.max_concurrent_threads_per_session must be a positive integer.",
            )
        )
    elif concurrent > 4:
        findings.append(
            Finding(
                "warning",
                "codex-agent-concurrency-high",
                ".codex/config.toml",
                f"Subagent concurrency is {concurrent}, above the conservative default of 3–4.",
                "Reduce concurrency unless parallel scopes and cost are explicitly justified.",
            )
        )

    secret_excludes = _nested(config, "shell_environment_policy", "ignore_default_excludes")
    if secret_excludes is not False:
        findings.append(
            Finding(
                "warning",
                "codex-secret-env-filter",
                ".codex/config.toml",
                "Automatic secret-name environment exclusions are not explicitly enabled.",
                "Set shell_environment_policy.ignore_default_excludes=false or document a narrowly scoped need.",
            )
        )
    return findings


def _check_custom_agents(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    expectations = {
        "repo-explorer.toml": "read-only",
        "reviewer.toml": "read-only",
        "executor.toml": "workspace-write",
    }
    for filename, expected_sandbox in expectations.items():
        path = root / ".codex" / "agents" / filename
        config, error = _load_toml(path)
        if error or config is None:
            if path.exists():
                findings.append(Finding("error", "custom-agent-invalid", _rel(path, root), f"Cannot parse: {error}"))
            continue
        for key in ("name", "description", "developer_instructions"):
            if not isinstance(config.get(key), str) or not config[key].strip():
                findings.append(
                    Finding("error", "custom-agent-field", _rel(path, root), f"Custom agent requires non-empty {key}.")
                )
        sandbox = config.get("sandbox_mode")
        if sandbox != expected_sandbox:
            severity = "error" if filename in {"repo-explorer.toml", "reviewer.toml"} else "warning"
            findings.append(
                Finding(
                    severity,
                    "custom-agent-sandbox",
                    _rel(path, root),
                    f"Expected sandbox_mode {expected_sandbox!r}, found {sandbox!r}.",
                )
            )
    return findings


def _check_pr_template(root: Path) -> list[Finding]:
    path = root / ".github" / "PULL_REQUEST_TEMPLATE.md"
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8").lower()
    except (OSError, UnicodeError) as exc:
        return [Finding("error", "pr-template-read", _rel(path, root), str(exc))]

    requirements = {
        "plain-language summary": ("plain-language", "summary"),
        "scope and non-goals": ("scope", "non-goal"),
        "test evidence": ("test", "expected", "actual", "evidence"),
        "risk/operational impact": ("risk", "rollback"),
        "documentation/governance": ("documentation", "agent"),
    }
    findings: list[Finding] = []
    for label, terms in requirements.items():
        if not all(term in text for term in terms):
            findings.append(
                Finding(
                    "error",
                    "pr-template-section",
                    _rel(path, root),
                    f"Pull-request template is missing the required {label} evidence.",
                )
            )
    return findings


def _check_docs(root: Path) -> list[Finding]:
    docs = root / "docs"
    if not docs.is_dir():
        return []
    findings: list[Finding] = []
    for path in sorted(docs.rglob("*.md")):
        rel_path = _rel(path, root)
        filename = path.name
        if filename != "README.md":
            pattern = ADR_NAME_RE if "decisions" in path.relative_to(docs).parts else DOC_NAME_RE
            if not pattern.match(filename):
                findings.append(
                    Finding(
                        "warning",
                        "doc-name",
                        rel_path,
                        "Documentation filename does not follow kebab-case or ADR numbering.",
                    )
                )
        if "template" in filename:
            continue
        try:
            head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:30]).lower()
        except (OSError, UnicodeError) as exc:
            findings.append(Finding("error", "doc-read", rel_path, str(exc)))
            continue
        for label in ("status:", "owner:", "last validated:", "validated by:"):
            if label not in head:
                findings.append(
                    Finding(
                        "warning",
                        "doc-metadata",
                        rel_path,
                        f"Authoritative-document metadata is missing {label[:-1]!r} near the top.",
                        "Add status, owner, last validation date, and executable/evidence validation source, or mark the document as a template/generated exception.",
                    )
                )
    return findings


def _check_tracked_artifacts(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for rel_path in _tracked_files(root):
        normalized = rel_path.replace("\\", "/")
        path = Path(normalized)
        lower = normalized.lower()
        name = path.name.lower()

        safe_env = name in {".env.example", ".env.template", ".env.sample"}
        if (name == ".env" or name.startswith(".env.")) and not safe_env:
            findings.append(
                Finding(
                    "error",
                    "tracked-env-file",
                    normalized,
                    "Environment file that may contain secrets is tracked by Git.",
                    "Remove it from tracking, rotate any exposed credentials, and retain only a value-free example/template.",
                )
            )
        if name in {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519"} or path.suffix.lower() in {".p12", ".pfx", ".key"}:
            findings.append(
                Finding(
                    "error",
                    "tracked-private-key",
                    normalized,
                    "Private-key-like file is tracked by Git.",
                    "Treat as exposed until proven otherwise, rotate/revoke, and remove using the approved history-remediation process.",
                )
            )
        if path.suffix.lower() == ".log":
            findings.append(
                Finding(
                    "warning",
                    "tracked-log",
                    normalized,
                    "Log file is tracked and may be stale, large, or sensitive.",
                    "Keep deterministic sanitized fixtures only; move operational logs to the approved logging/retention system.",
                )
            )
        if any(part in {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules"} for part in path.parts):
            findings.append(
                Finding("warning", "tracked-cache", normalized, "Local dependency/cache output is tracked by Git.")
            )
        if lower.startswith("artifacts/repo-audit/") or lower.startswith("artifacts/repository-standard/"):
            findings.append(
                Finding(
                    "warning",
                    "tracked-audit-artifact",
                    normalized,
                    "Generated audit output is tracked in the active repository.",
                    "Keep generated audit reports gitignored unless a reviewed result is intentionally promoted to an authoritative artifact.",
                )
            )
    return findings


def validate_repository(root: Path) -> list[Finding]:
    root = root.resolve()
    findings: list[Finding] = []
    if not root.is_dir():
        return [Finding("error", "root-invalid", str(root), "Repository root is not a directory.")]

    findings.extend(_check_required(root))
    manifest_findings, manifest = _check_manifest(root)
    findings.extend(manifest_findings)
    findings.extend(_check_agents_md(root, manifest))
    findings.extend(_check_instruction_files(root, manifest))
    findings.extend(_check_skills(root, manifest))
    findings.extend(_check_codex_config(root, manifest))
    findings.extend(_check_custom_agents(root))
    findings.extend(_check_pr_template(root))
    findings.extend(_check_docs(root))
    findings.extend(_check_tracked_artifacts(root))
    return sorted(findings, key=lambda item: ({"error": 0, "warning": 1, "info": 2}.get(item.severity, 9), item.path, item.code))


def _summary(findings: Sequence[Finding]) -> dict[str, int]:
    counts = {"error": 0, "warning": 0, "info": 0}
    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1
    return counts


def _print_text(root: Path, findings: Sequence[Finding]) -> None:
    counts = _summary(findings)
    print(f"Repository standard validation: {root}")
    print(f"Errors: {counts['error']}  Warnings: {counts['warning']}  Info: {counts['info']}")
    if not findings:
        print("PASS: no findings")
        return
    for finding in findings:
        print(f"\n[{finding.severity.upper()}] {finding.code}: {finding.path}")
        print(f"  {finding.message}")
        if finding.remediation:
            print(f"  Remediation: {finding.remediation}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root (default: current directory).")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as validation failures.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit machine-readable JSON.")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    findings = validate_repository(root)
    counts = _summary(findings)
    failed = counts["error"] > 0 or (args.strict and counts["warning"] > 0)

    if args.json_output:
        payload = {
            "standard": STANDARD_ID,
            "root": str(root),
            "strict": args.strict,
            "passed": not failed,
            "summary": counts,
            "findings": [asdict(item) for item in findings],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_text(root, findings)
        print("\nRESULT:", "FAIL" if failed else "PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

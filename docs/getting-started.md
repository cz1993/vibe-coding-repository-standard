# Get started with VCRS in 15 minutes

This guide uses the safest path: inspect first, change later.

## What you need

- Git;
- Python 3.11 or newer for the included validators;
- a coding agent, with the current reference prompts written for OpenAI Codex;
- a project repository you are allowed to inspect.

You do **not** need an MCP server, persistent memory, hooks, a database connection, or production access.

## Step 1: download VCRS

Clone or download this repository somewhere outside the project you want to review.

Keep the standard and the target repository separate. Do not copy an old repository inside a new one as an `archive/` directory; that can pollute searches and agent context.

## Step 2: validate the included starter

From the VCRS root, run:

```bash
python standard/template/scripts/maintenance/validate_repository_standard.py \
  --root standard/template

python -m unittest discover \
  -s standard/template/tests/standards \
  -p 'test_*.py' \
  -v
```

This confirms that the reference template and its validator work in your local Python environment. It does not inspect your application.

## Step 3: choose the right path

### Existing or vibe-coded repository

Open [`../standard/prompts/01-bootstrap-repository.prompt.md`](../standard/prompts/01-bootstrap-repository.prompt.md) and set:

```text
PROJECT_ROOT=<absolute path to your project>
STANDARD_KIT_PATH=<absolute path to this VCRS repository>
MODE=audit-only
GIT_ACTION=none
```

Use `audit-only` first. The agent should inventory the repository, identify risks and unknowns, select a profile, and propose a minimal baseline without editing application code.

### Several repositories

Use [`../standard/prompts/00-machine-wide-rollout.prompt.md`](../standard/prompts/00-machine-wide-rollout.prompt.md) with:

```text
MODE=inventory-only
GIT_ACTION=none
```

Limit the scan to an explicit projects directory. Do not authorize whole-disk traversal.

### New repository

Review [`../standard/template/`](../standard/template/) and copy only the relevant governance files. Replace every placeholder and remove any section your project does not need.

## Step 4: review the proposal as a human

Before allowing edits, confirm that the proposal:

- preserves existing uncommitted work;
- does not access production, secrets, or private data;
- identifies actual entry points and commands;
- distinguishes facts, inferences, and unknowns;
- avoids mass moves, renames, and dependency upgrades;
- keeps optional MCP, memory, and hooks disabled;
- explains which files will be added or changed;
- includes a validation plan.

A clean-looking proposal is not enough. It should cite repository evidence.

## Step 5: apply on a branch or worktree

After accepting the audit, rerun with:

```text
MODE=audit-and-apply
GIT_ACTION=commit
```

Use a dedicated branch or worktree. Review the complete diff before committing.

## Step 6: use the normal change cycle

For later development, use [`../standard/prompts/02-multi-agent-change-cycle.prompt.md`](../standard/prompts/02-multi-agent-change-cycle.prompt.md).

A material change should produce:

1. a bounded task contract;
2. a trace of the relevant flow;
3. an implementation diff;
4. scenario-level test evidence;
5. an independent review;
6. a re-review after accepted fixes.

## Stop conditions

Stop and investigate instead of continuing when:

- the repository has unprotected uncommitted work;
- a command might deploy, migrate, delete, charge money, or contact live systems;
- credentials appear in output;
- the agent cannot determine which source is authoritative;
- an apparently unused script may have an external caller;
- the proposed bootstrap changes application behavior;
- the validator passes but the project tests fail.

## What success looks like

A successful first adoption is modest. You should be able to answer:

- What does this repository do?
- How do I run the safe local checks?
- Where are the permanent agent rules?
- Which documents are authoritative?
- What are the main entry points and side effects?
- Which optional capabilities remain disabled?
- How will the next change be reviewed?

That is enough to begin improving the repository without pretending all uncertainty is gone.

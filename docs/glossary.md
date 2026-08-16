# Glossary

## Agent instruction file

A version-controlled file that gives a coding agent persistent rules for work in a repository. In the Codex reference implementation, the canonical file is `AGENTS.md`.

## Agent skill

A focused, reusable workflow that an agent loads when a task matches its purpose. A skill should have clear trigger and non-trigger conditions, inputs, outputs, and completion criteria.

## Audit-first bootstrap

A process that inventories and understands an existing repository before applying a standard or restructuring files.

## Characterization test

A test that records current behavior, including behavior that may later be improved. It reduces the risk of accidental changes during refactoring.

## Context debt

The maintenance cost created when instructions, documentation, scripts, and historical notes no longer provide a current and coherent explanation of the repository.

## Contract test

A test that verifies an interface or observable agreement, such as an API response, file schema, database boundary, or message format.

## Continuity

Evidence that a new, lite, migrated, or refactored repository still provides the required behavior and operational capabilities of the prior system.

## Executor

The agent or person responsible for implementing one bounded change and producing validation evidence.

## Explorer

A read-only role that maps entry points, dependencies, side effects, contracts, and unknowns before implementation.

## Generative engine optimization (GEO)

An emerging term for improving how content is discovered, selected, cited, or used by generative answer systems. Evidence and metrics remain unsettled; VCRS treats it as clear information design and source quality, not a guaranteed ranking method.

## MCP

Model Context Protocol, a protocol for connecting AI applications to tools and data sources. An MCP server can be useful, but it also introduces permission, privacy, execution, and context considerations.

## Normative

A requirement that defines conformance to the standard. VCRS uses terms such as REQUIRED, RECOMMENDED, and OPTIONAL in its detailed handbook.

## Orchestrator

The human or agent that owns task framing, acceptance criteria, role boundaries, and the final decision. The orchestrator should not hide unresolved evidence or let an executor approve its own work.

## Profile

A set of additional questions and evidence expectations for a repository type, such as a monorepo or data platform. A profile does not force a universal source tree.

## Repository operating surface

The files and workflows that explain how a repository is understood, changed, tested, reviewed, secured, and maintained.

## Reviewer

An independent role that examines the task contract, complete diff, assumptions, and evidence. The reference reviewer is read-only and leads with concrete, ranked findings.

## Source of truth

The authoritative location for a kind of information. Different facts can have different sources of truth: migrations for database history, configuration for schedules, tests for contracts, and decision records for rationale.

## Vibe coding

A development style in which a person directs an AI coding agent largely through natural-language intent and iterative feedback. The human may not manually author or fully inspect every line.

# Frequently asked questions

## What is Vibe Coding Repository Standard?

VCRS is an open-source repository operating standard, starter template, validator, and agent workflow. It helps people turn an AI-built or fast-growing codebase into a repository that is easier to understand, test, review, and maintain.

## Is VCRS a programming framework?

No. It does not replace React, Django, .NET, Rails, Terraform, or another application framework. It standardizes the repository's governance and evidence surface while preserving language-native conventions.

## Does VCRS force one folder structure?

No. It defines a small mandatory governance core and offers profiles for single applications, monorepos, data platforms, and infrastructure repositories. Application source stays aligned with the project's actual stack.

## Is VCRS only for OpenAI Codex?

The principles are agent-compatible, but the current reference implementation is Codex-first. Files for other agents should be treated as adapters and tested before compatibility is claimed.

## Do I need multiple agents?

No. Small or low-risk changes may only need one executor plus human review. The explorer and independent reviewer roles become valuable when the repository is unfamiliar, the change is material, or the cost of a missed defect is high.

## Why should the reviewer be read-only?

A read-only reviewer is less likely to blur authorship and approval. It can focus on finding defects, checking evidence, and comparing the result with the task contract. Accepted fixes return to the executor and are reviewed again.

## Should I delete old documentation and scripts?

Not until their current role has been investigated. Git history or an external evidence archive is usually a better home for stale material, but an apparently unused script may still be invoked by a scheduler, deployment platform, or operator.

## Is a “lite” copy of my repository a good fresh start?

It can be a useful candidate. Treat it as unverified until critical capabilities, data contracts, migrations, schedules, and operational procedures have been reconciled with the original repository and deployed environment.

## How long should `AGENTS.md` be?

There is no universal ideal number. VCRS recommends a deliberately small byte budget and only information every task needs. Put repeatable specialized workflows in skills, enforceable rules in tests or CI, decisions in decision records, and temporary state in issues or pull requests.

## Should I enable persistent memory?

Not by default. Required team guidance belongs in version-controlled repository files. Memory can be useful for non-critical personal recall after the repository is stable, but it should not become the sole source of truth or contain secrets.

## Should I install every useful MCP server?

No. Each server expands the tool, permission, and context surface. Admit it for a specific need, constrain it to the minimum environment and data, separate read from write actions, test rollback, and set a review date.

## Does passing the VCRS validator mean my application is correct?

No. The validator checks objective parts of the repository operating surface. It cannot prove application behavior, security, performance, or production readiness.

## Does VCRS replace tests?

No. It makes tests and their relationship to requirements more visible. Critical workflows still need appropriate unit, contract, integration, smoke, migration, or recovery tests.

## Can VCRS help clean up an overengineered codebase?

Yes, after behavior is understood. The included supplemental review looks for speculative abstractions, duplicate utilities, unnecessary dependencies, and broad refactors while protecting validation, security, observability, migrations, recovery, and useful tests.

## Is VCRS useful for non-developers?

Yes, especially for product owners and vibe coders who need a clearer way to direct agents and review evidence. It does not remove the need to learn the product domain or to involve engineering and security expertise as risk grows.

## Will the SEO or GEO files guarantee more visibility?

No. Helpful, accurate, well-structured content can improve discoverability, but search engines and generative systems make independent and changing decisions. VCRS includes a practical discovery guide and an experimental `llms.txt` source map without presenting either as a ranking guarantee.

## How do I ask for help?

Use GitHub Discussions for questions and adoption stories. Use an issue for a reproducible defect, broken link, validator problem, or concrete proposal. Never paste credentials, private repository content, customer data, or production logs into a public report.

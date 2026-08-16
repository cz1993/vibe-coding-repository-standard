# Source Register

**Last researched:** 2026-08-15  
**Review cadence:** Quarterly, because Codex and MCP configuration can change.

This register records the principal external guidance used to develop and publish VCRS. It is not copied into project `AGENTS.md` files.

## OpenAI Codex

### Custom instructions with `AGENTS.md`

URL: https://developers.openai.com/codex/agent-configuration/agents-md

Key use:

- Codex reads global and project instructions through a hierarchy.
- It checks `AGENTS.override.md`, `AGENTS.md`, and configured fallback names while walking from repository root toward the working directory.
- Closer instructions can take precedence.

Standard implication: use canonical filenames, inspect nested instruction files, avoid fallback aliases, and keep the always-loaded instruction surface small.

### Build skills

URL: https://developers.openai.com/codex/build-skills

Key use:

- Skills load by progressive disclosure.
- `SKILL.md` requires `name` and `description`.
- Skill descriptions need clear trigger boundaries.
- OpenAI recommends one job per skill, explicit inputs/outputs, and trigger testing.
- `agents/openai.yaml` can disable implicit invocation and declare dependencies.
- The initial skill list has a bounded context budget, so large catalogs can be shortened or omitted.

Standard implication: begin with three narrowly scoped root skills and make broad/expensive workflows explicit.

### Subagents

URL: https://developers.openai.com/codex/subagents

Key use:

- Project custom agents can live under `.codex/agents`.
- Agent files support a name, description, developer instructions, sandbox mode, and other selected configuration.
- Read-only explorer and reviewer roles are documented patterns.
- Subagents inherit unspecified parent settings, so parent permissions matter.

Standard implication: separate explorer, executor, and reviewer roles; keep review read-only and parent permissions conservative.

### Codex best practices

URL: https://developers.openai.com/codex/learn/best-practices

Key use:

- Use one coherent task per chat.
- Give goals, context, constraints, and completion criteria.
- Use planning and verification for complex work.
- Avoid broad permissions too early and use worktrees for parallel work.

Standard implication: task contracts, bounded development cycles, safe defaults, and explicit completion evidence.

### Customization overview

URL: https://developers.openai.com/codex/customization/overview

Key use: distinguishes persistent instructions, memories, skills, MCP, and subagent customization layers.

Standard implication: place knowledge and capability in the narrowest appropriate layer rather than accumulating everything in `AGENTS.md`.

### Configuration reference

URL: https://developers.openai.com/codex/config-reference

Key use:

- defines approval, sandbox, instruction budget, fallback filenames, memories, hooks, multi-agent settings, and concurrency keys;
- confirms outbound network control for the workspace-write sandbox.

Standard implication: the template uses current safe baseline keys and must be revalidated at each standard release.

### Codex MCP server / Agents SDK integration

URL: https://developers.openai.com/codex/mcp-server

Key use: Codex can be exposed through an MCP server for more deterministic orchestration using the Agents SDK.

Standard implication: available as a future advanced orchestration option, not required for the baseline executor/reviewer flow.

## Reference repositories

### Ponytail

Repository: https://github.com/DietrichGebert/ponytail  
Primary instruction source: https://raw.githubusercontent.com/DietrichGebert/ponytail/main/AGENTS.md

Key use:

- trace the actual execution flow;
- prefer YAGNI, reuse, existing platform capabilities, and small diffs;
- solve root causes;
- do not remove validation, error handling, security, or accessibility;
- use runnable checks for non-trivial logic.

Caution: its specialized overengineering review intentionally does not cover every correctness, security, or performance concern. “Fewest files” is not an appropriate universal metric for operationally important tests, migrations, contracts, and runbooks.

Standard implication: incorporate its strongest principles into `safe-change`; use an optional explicit overengineering pass only as supplemental review.

### Codebase Memory MCP

Repository: https://github.com/DeusData/codebase-memory-mcp  
README: https://raw.githubusercontent.com/DeusData/codebase-memory-mcp/main/README.md

Key use: local persistent code graph, structural navigation, impact analysis, and several agent integrations.

Cautions identified from its repository documentation:

- installer can modify Codex config and add instructions, skills, agents, hooks, and daemon behavior;
- indexing/watch behavior and mutating management tools require governance;
- clean recorded coverage is not proof of complete/current indexing;
- uninstall and owned-configuration cleanup need testing.

Standard implication: optional project-specific trial in an isolated profile, with explicit indexing, narrow read-only tools, benchmarks, and rollback.

## Model Context Protocol

### Client best practices

URL: https://modelcontextprotocol.io/docs/2026-07-28/develop/clients/client-best-practices

Key use: large upfront tool catalogs consume context and can reduce performance; progressive discovery and dynamic server connection are recommended as tool counts grow.

Standard implication: keep a minimal always-on capability set and connect/discover broader tools only when needed.

### Security best practices

URL: https://modelcontextprotocol.io/docs/draft/tutorials/security/security_best_practices

### Authorization

URL: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/authorization

### Specification

URL: https://modelcontextprotocol.io/specification/2025-03-26

Key use: external tools create authorization, data, code-execution, and consent risks.

Standard implication: least privilege, explicit approval, read/write separation, constrained outputs, safe credential handling, and admission records.

## Engineering and review practice

### Google Engineering Practices — What to look for in a code review

URL: https://google.github.io/eng-practices/review/reviewer/looking-for.html

Key use: review design, functionality, complexity, tests, naming, comments, documentation, context, and every relevant line; avoid speculative overengineering and combine tests with production changes.

### Google Engineering Practices — Small changes

URL: https://google.github.io/eng-practices/review/developer/small-cls.html

Key use: small coherent changes are easier to understand, review, test, merge, and roll back.

### Google Engineering Practices — Standard of review

URL: https://google.github.io/eng-practices/review/reviewer/standard.html

Key use: code review aims to improve system health; technical facts and evidence take priority over preferences.

Standard implication: one coherent PR, independent review, evidence-backed severity, and no blocking preference-only comments.

## GitHub repository governance

### Template repositories

URL: https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository

Key use: a template can reproduce directory structure, branches, and files for new repositories with unrelated history.

Standard implication: use templates for new repos, not as the update mechanism for existing repos.

### Pull-request templates

URL: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository

### Protected branches

URL: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule

Key use: standardize evidence and require reviews/status checks.

## Documentation and architecture

### Diátaxis

URL: https://diataxis.fr/

Key use: separates tutorials, how-to guides, explanation, and reference according to reader need.

Standard implication: the active docs tree distinguishes architecture explanation, operational runbooks, and exact reference; tutorials are added only when needed.

### C4 model

URL: https://c4model.com/

Key use: hierarchical software architecture views from system context to containers/components/code.

Standard implication: document the system and major boundaries without producing one unreadable diagram of every implementation detail.

### Microsoft architectural principles

URL: https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles

Key use: separation of concerns, encapsulation, dependency inversion, and explicit dependencies.

### AWS hexagonal architecture guidance

URL: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html

Key use: isolate application policy from external interfaces to improve loose coupling and testability.

### AWS Well-Architected operational excellence

URL: https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html

Key use: operations as code, small reversible changes, failure anticipation, and continuous improvement.

### CISA Secure by Design

URL: https://www.cisa.gov/securebydesign

Key use: security should be a core product requirement and safe defaults should reduce the burden on users.

Standard implication: security and data integrity precede pattern purity; production privileges and external tools are disabled by default.


## Public open-source release and discovery

### GitHub repository best practices and README guidance

URLs:

- https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

Key use: a clear README, license, contribution path, security policy, and focused repository scope make a public project easier to evaluate and maintain.

Standard implication: the root README answers what, why, who, how to start, limitations, support, and contribution questions before exposing the detailed handbook.

### GitHub topics and social preview

URLs:

- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview

Key use: accurate topics and a readable social-preview image improve recognition and discovery on GitHub and when links are shared.

Standard implication: use a focused topic set, one consistent project identity, and the included 1280×640 public preview image.

### GitHub community health, citation, and vulnerability reporting

URLs:

- https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
- https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository

Key use: community files establish contribution, conduct, support, and security expectations; citation metadata makes releases easier to reference; private vulnerability reporting keeps sensitive reports out of public issues.

Standard implication: publish the community-health files in the repository, provide `CITATION.cff`, and enable private vulnerability reporting after the repository is created.

### Google Search and AI-feature guidance

URL: https://developers.google.com/search/docs/appearance/ai-features

Key use: Google's current guidance for AI search experiences continues to rely on normal search eligibility, crawlable text, helpful people-first content, and established SEO fundamentals. It does not require a special AI text file or special schema.

Standard implication: optimize for clear answers, original evidence, accurate titles, internal links, and maintained content. Treat `llms.txt` as an optional source map rather than a ranking mechanism.

### Google Search Essentials and title guidance

URLs:

- https://developers.google.com/search/docs/essentials
- https://developers.google.com/search/docs/appearance/title-link

Key use: search eligibility is not guaranteed; descriptive, concise titles, crawlable internal links, useful text, and participation in relevant communities are durable foundations. Keyword stuffing and vague titles are not.

Standard implication: use plain problem-oriented headings, natural terminology, accurate internal links, and useful community participation. Do not promise indexing or rankings.

### Generative-engine optimization evidence

URLs:

- https://arxiv.org/abs/2607.14035
- https://arxiv.org/abs/2602.12187
- https://arxiv.org/abs/2603.29979

Key use: recent research suggests that document structure and already-retrieved content can affect citation behavior, but the evidence is conditional and pipeline-dependent. A July 2026 critical survey found no reviewed technique with a stable, longitudinal, cross-platform causal effect on organic discoverability or downstream behavior; realistic end-to-end evaluation also shows that generation-oriented changes can harm retrieval or reranking.

Standard implication: make content clear, structured, truthful, text-accessible, and source-backed because those qualities help people and may help machine retrieval. Treat GEO as an experimental measurement problem, not a guaranteed ranking recipe. Repeat tests across prompts, engines, and dates, and never use hidden instructions or misleading content.

### `llms.txt` community proposal

URL: https://llmstxt.org/

Key use: `llms.txt` is a community convention for publishing a concise machine-readable source map. It is not a formal web standard, crawler-control mechanism, or prerequisite for Google AI features.

Standard implication: keep the file small, factual, and optional. The authoritative content remains the human-readable repository and its normal access controls.

### GitHub explanation of vibe coding

URL: https://github.com/resources/articles/ai/what-is-vibe-coding

Key use: provides a current public description of the natural-language, AI-guided development style addressed by the project.

Standard implication: describe vibe coding neutrally, preserve its accessibility benefits, and focus VCRS on the understanding and verification gap that can appear as projects mature.

### OpenSSF project health guidance

URLs:

- https://securityscorecards.dev/
- https://www.bestpractices.dev/

Key use: public projects benefit from explicit security policy, maintained dependencies and workflows, branch review controls, and verifiable project-health practices.

Standard implication: begin with minimal workflow permissions, dependency-update visibility, publication checks, and a documented security-reporting route; adopt additional controls when the repository's risk and contributor model justify them.

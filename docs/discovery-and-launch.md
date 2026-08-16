# Discovery and launch guide

This guide improves the chance that the right users can find and understand VCRS. It does not promise rankings, citations, stars, traffic, or adoption.

## Product identity

Use one consistent entity name:

- **Full name:** Vibe Coding Repository Standard
- **Acronym:** VCRS
- **Recommended repository slug:** `vibe-coding-repository-standard`
- **Tagline:** Build fast with AI. Keep the repository understandable.
- **Category:** open-source community repository operating standard and starter kit
- **Reference implementation:** OpenAI Codex
- **Status:** public preview

The recommended slug is not reserved by this project plan. Recheck GitHub immediately before creation and consider a basic trademark search before investing heavily in the brand.

## Recommended GitHub description

Use this concise description:

> Open-source repository standard, starter template, validator, and multi-agent workflow for making vibe-coded and AI-generated software understandable, testable, reviewable, and maintainable. Codex-first reference implementation.

## Recommended GitHub topics

GitHub supports up to 20 topics. Start with a focused set rather than using every related term:

```text
vibe-coding
ai-coding
coding-agents
agentic-development
repository-template
repository-standards
codex
agents-md
multi-agent
code-review
software-maintenance
developer-tools
prompt-engineering
mcp
open-source
```

Revisit topics from actual search and referral data. Do not add unrelated trending topics.

## Social preview

Upload [`../assets/social-preview.png`](../assets/social-preview.png) through repository settings. It is designed at 1280×640 pixels with readable text and a safe central area for social crops.

The README uses [`../assets/vcrs-hero.svg`](../assets/vcrs-hero.svg) because SVG stays sharp on GitHub. The PNG is the social-sharing asset.

## GitHub repository settings

Before launch:

- set visibility to public only after the release audit passes;
- enable Issues and Discussions;
- enable private vulnerability reporting;
- set default Actions permissions to read repository contents;
- require approval for workflows from first-time contributors;
- protect `main` with pull-request review and required quality checks;
- enable Dependabot alerts and security updates when appropriate;
- disable unused features rather than leaving empty surfaces;
- add the description, website when one exists, topics, and social preview;
- review the Community Standards checklist after publication.

Suggested Discussion categories:

- Announcements;
- Q&A;
- Adoption stories;
- Ideas and proposals;
- Show and tell.

## Search-engine optimization

The repository follows durable search practices rather than tricks:

1. **Answer a real problem clearly.** The README explains what VCRS is, who it is for, why it is useful, how to start, where to get help, and who maintains it.
2. **Use descriptive titles and headings.** Pages have one clear topic and natural language that matches how users describe the problem.
3. **Use relevant terms in context.** Phrases such as “vibe coding best practices,” “AI coding agent repository structure,” and “multi-agent code review” appear only where they help explain the content.
4. **Create crawlable internal links.** The README, white paper, guides, FAQ, glossary, standard, and source register link to one another.
5. **Keep content current.** Version, status, research date, compatibility, and limitations are explicit.
6. **Earn external references.** Publish useful adoption examples, answer community questions, and invite expert review instead of manufacturing links.
7. **Avoid keyword stuffing.** Repetition that harms readability can reduce trust and search quality.

A GitHub repository has limited control over HTML metadata and structured data. A future documentation site can add unique page titles, descriptions, canonical URLs, an XML sitemap, and appropriate structured data. Do not add misleading schema or invisible text.

## Generative-engine discoverability

Generative engine optimization (GEO) is emerging and evidence remains conditional. The practical VCRS approach is:

- provide direct definitions and answers;
- use descriptive sections and short summary tables;
- support claims with primary or authoritative sources;
- make limitations and dates explicit;
- keep important content available as text, not only images;
- use stable terminology across README, white paper, citation metadata, releases, and external posts;
- include examples, procedures, comparisons, and evidence that can be quoted accurately;
- maintain a source register;
- measure across repeated prompts and platforms instead of relying on one result.

The repository includes `llms.txt` as a low-cost curated source map. It is a community proposal, not a W3C or IETF standard, access-control mechanism, crawler directive, or ranking guarantee. Google states that no special AI text file or markup is required for its AI search features; normal search eligibility and people-first content remain the foundation.

## Content plan after launch

High-value follow-up content should come from real adoption:

1. **A small repository case study:** setup time, files changed, what was unnecessary.
2. **A complex repository recovery:** anonymized context debt, unknown scripts, continuity gates, and measured results.
3. **A comparison guide:** what belongs in `AGENTS.md`, a skill, MCP, a test, a decision record, or a runbook.
4. **A failure story:** a rule or workflow that created ceremony and was removed.
5. **Agent adapter reports:** tested behavior and limitations for another tool.
6. **Short tutorials:** first hour, first audit, first independent review, and first quarterly cleanup.

Each page should solve one question rather than repeating the entire project description.

## Launch sequence

### Pre-launch

- complete [`publication-audit.md`](publication-audit.md);
- validate every command in the README;
- create the GitHub repository with no imported private history;
- configure security and branch settings;
- upload the social preview;
- add topics and description;
- create release `v0.1.0` from the audited commit.

### Launch message structure

A useful announcement should contain:

1. the problem: fast AI-built repositories become hard to understand;
2. the promise: preserve speed while adding truth, evidence, and review;
3. what is included: standard, template, prompts, roles, validator, and guides;
4. who it helps;
5. one concrete starting action;
6. public-preview limitations;
7. a request for adoption evidence and feedback.

Avoid claiming “the universal standard,” “production safety,” or guaranteed productivity improvements.

### Community channels

Share where the problem is already being discussed and follow each community's self-promotion rules. Good contributions to a community are more durable than posting the same launch copy everywhere. Answer questions, publish measurements, and be transparent about AI assistance and project limitations.

## Measurement

Track useful outcomes, not only vanity metrics:

- README-to-getting-started navigation;
- clones, unique visitors, stars, forks, and contributors;
- issue quality and FAQ gaps;
- external citations and referring domains;
- search queries and documentation page visits if a site is launched;
- repeated AI-answer citation tests with controlled prompts;
- actual adoption reports;
- time to first successful audit or validator run;
- retention of contributors and maintainers.

Record baseline dates and avoid attributing a change to SEO or GEO without a reasonable comparison.

## Source basis

This guide follows GitHub's README and community-health guidance, Google Search Essentials and AI-feature guidance, and recent GEO research. The dated links and cautions are recorded in [`../standard/handbook/09-source-register.md`](../standard/handbook/09-source-register.md).

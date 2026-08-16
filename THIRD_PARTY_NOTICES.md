# Third-party notices and acknowledgments

Vibe Coding Repository Standard (VCRS) is original work released under Apache-2.0. It refers to external documentation and open-source projects for research, comparison, interoperability, and acknowledgment.

## No vendored third-party source

Version 0.1.0 does not intentionally vendor source code from the projects listed below. Links and concise factual descriptions are retained so readers can inspect the primary sources. General software-engineering ideas—such as small changes, clear ownership, least privilege, independent review, and avoiding speculative abstraction—are not represented as exclusive inventions of VCRS.

## Referenced open-source projects

### Ponytail

- Project: https://github.com/DietrichGebert/ponytail
- License observed during the release audit: MIT
- Relationship: VCRS discusses a similar minimal-change discipline: trace real behavior, solve demonstrated problems, reuse existing capabilities, and do not remove safety work merely to reduce file count.
- No Ponytail source code is included.

### Codebase Memory MCP

- Project: https://github.com/DeusData/codebase-memory-mcp
- License observed during the release audit: MIT
- Relationship: VCRS includes an isolated admission-trial prompt for measuring whether structural codebase indexing provides enough value to justify its context, permission, installation, and maintenance costs.
- No Codebase Memory MCP source code is included.

### OpenAI Codex

- Project and documentation: https://github.com/openai/codex and https://developers.openai.com/codex
- Relationship: the current reference implementation uses Codex-compatible instruction, skill, subagent, configuration, and prompt conventions.
- VCRS is an independent community project. Reference to Codex does not imply sponsorship, endorsement, certification, or affiliation with OpenAI.

## Documentation and standards references

VCRS links to official or primary materials from OpenAI, GitHub, Google, Microsoft, the Model Context Protocol project, OpenSSF, CISA, C4, Diátaxis, Google Engineering Practices, and others. The dated source register records the materials consulted and the conclusions drawn from them.

External materials remain subject to their own copyright, license, and trademark terms. A link or summary does not relicense the referenced material under Apache-2.0.

## Trademarks

OpenAI, Codex, GitHub, Ponytail, Codebase Memory MCP, and other names are the property of their respective owners. Their use here is descriptive and does not imply sponsorship, endorsement, compatibility certification, or affiliation.

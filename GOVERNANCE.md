# Governance

VCRS uses lightweight, transparent governance suitable for an early open-source standard.

## Roles

### Contributors

Anyone who improves documentation, code, tests, examples, profiles, prompts, research, or adoption evidence.

### Reviewers

Trusted contributors who regularly provide evidence-based review in a defined area. Review status does not automatically grant release or repository administration access.

### Maintainers

People with authority to merge changes, manage releases, moderate community spaces, and make time-sensitive security decisions. Maintainer identity is represented by Git history and repository permissions rather than hard-coded personal information in this package.

## Decision principles

Maintainers should prefer decisions that:

1. improve repository legibility or safety for real users;
2. are supported by evidence or a clearly stated experiment;
3. preserve backward compatibility when reasonable;
4. keep the permanent context layer small;
5. avoid tool lock-in and unsupported compatibility claims;
6. can be implemented, reviewed, and maintained by the community;
7. make migration and removal possible.

## Types of change

### Editorial change

Clarifies wording or navigation without changing the meaning of the standard. Normal pull-request review is sufficient.

### Implementation change

Changes validators, templates, prompts, or workflows without changing a normative requirement. It requires tests and compatibility review.

### Normative change

Adds, removes, or materially changes a MUST, SHOULD, profile requirement, safety boundary, or adoption expectation. It should begin with a public proposal and include:

- problem statement;
- evidence;
- proposed wording;
- alternatives;
- compatibility impact;
- migration plan;
- validation plan.

### Security change

May be handled privately until a coordinated release is ready.

## Decision process

The normal process is rough consensus supported by maintainer judgment. Consensus does not require unanimity. Maintainers should summarize substantial disagreements and the reason for the final decision.

For a contested normative change, maintainers may request:

- a time-bounded experiment;
- more adoption evidence;
- a compatibility adapter rather than a core change;
- a minor or major version boundary;
- rejection with a documented rationale.

## Versioning

VCRS uses Semantic Versioning for the public package.

- Patch: corrections and compatible implementation improvements.
- Minor: new compatible capabilities, profiles, or guidance; while major version is `0`, some normative evolution may also occur here with migration notes.
- Major: stable-series breaking normative or structural changes.

## Conflicts of interest

Contributors should disclose material commercial or organizational interests when proposing a rule that could advantage a specific product or vendor. Compatibility references should be factual and non-exclusive.

## Project assets and trademarks

The project name and visual identity may be used to refer accurately to unmodified VCRS releases and compatible community work. Do not imply official endorsement, certification, or maintainer status without permission.

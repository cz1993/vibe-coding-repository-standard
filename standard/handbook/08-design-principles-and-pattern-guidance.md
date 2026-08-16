# Design Principles and Pattern Guidance

**Purpose:** Provide practical architecture guidance without turning SOLID or design patterns into mandatory ceremony.

## 1. Decision priority

Apply principles in this order:

1. protect correctness, security, privacy, and data integrity;
2. preserve explicit user and system contracts;
3. make the behavior understandable and testable;
4. keep changes small and reversible;
5. isolate real reasons to change;
6. reuse existing mechanisms after evidence;
7. add extension points for known variation;
8. optimize performance when measurement shows a need.

A simpler design is not better when it hides failures, weakens isolation, or removes evidence needed to operate a managed service.

## 2. KISS and YAGNI

### KISS

Choose the simplest design that fully satisfies current requirements and operational responsibilities. Simplicity includes:

- explicit behavior;
- few moving parts;
- clear ownership;
- discoverable entry points;
- good failure handling;
- testable boundaries;
- reversible operation.

A short script with hidden side effects may be less simple than a small module with a clear interface and tests.

### YAGNI

Do not build speculative generality. An abstraction should normally have:

- at least two real consumers or implementations; or
- one immediate, material boundary such as an external vendor, database, clock, filesystem, or queue; or
- a contractually required extension point.

Do not add plugin systems, generic repositories, event buses, or service boundaries for imagined future scale.

## 3. SOLID, applied pragmatically

### Single Responsibility Principle

Interpret responsibility as a **reason to change**, not “one method per class” or “one file per function.” A business capability module can contain several related operations if they change for the same domain reason.

Signals to split:

- unrelated stakeholders request changes;
- different security or deployment boundaries exist;
- tests require very different fixtures;
- one module coordinates policy and low-level vendor details;
- changes repeatedly touch unrelated concerns.

Do not split merely to reduce line count.

### Open/Closed Principle

Protect stable policy from known variations. Use an adapter, strategy, or data-driven rule when variation is real and active.

Do not pre-build extension frameworks for one implementation. The first change can remain direct; the second concrete variation often reveals the correct seam.

### Liskov Substitution Principle

Substitutes must preserve observable behavior and contract expectations. Protect this with contract tests covering:

- accepted inputs;
- outputs and errors;
- side effects;
- timing/idempotency assumptions where relevant;
- authorization and data isolation.

Inheritance is not required. The principle applies to interfaces, adapters, mocks, implementations, and compatible API versions.

### Interface Segregation Principle

Expose small interfaces shaped around consumer needs. Avoid a giant service object that grants every caller read, write, delete, and administrative behavior.

Do not create many one-method interfaces solely to claim compliance. Split when consumers genuinely need different capabilities or permissions.

### Dependency Inversion Principle

Core business policy should not depend directly on volatile technical details. Place boundaries around:

- databases;
- external APIs and vendor SDKs;
- clocks and schedulers;
- files/object storage;
- queues;
- identity providers;
- user-interface frameworks.

Do not wrap stable language/library primitives or every internal helper. The purpose is to protect important policy and testability, not maximize indirection.

## 4. Recommended default architecture

For most evolving business applications, begin with a **modular monolith**:

- one repository and deployable unit unless operations require otherwise;
- modules aligned to business capabilities;
- explicit internal boundaries;
- shared runtime infrastructure kept behind narrow APIs;
- contracts and tests at important module seams.

Move to independent services only when there is evidence for separate deployment, scaling, availability, security, ownership, or release cadence. Network boundaries add failure modes, latency, versioning, observability, and operational cost.

## 5. Functional core, imperative shell

Where useful:

- keep calculations, validation, normalization, policy evaluation, and state transitions deterministic;
- keep database, filesystem, network, scheduling, and UI operations in a thinner orchestration shell;
- test the core extensively with fixtures and property/boundary cases;
- integration-test the shell at critical seams.

Do not force pure-functional style when it obscures the domain or framework conventions.

## 6. External-boundary adapters

Use adapters for real external volatility:

```text
core policy -> application port -> database/vendor/file/UI adapter
```

An adapter should translate contracts and failures, not merely forward every call unchanged. Keep vendor-specific models out of core policy where they would create coupling.

## 7. Workflow and reliability patterns

### Explicit state machine

Use an explicit state model when work has meaningful transitions, retries, partial completion, approval, or recovery. Examples:

```text
planned -> running -> partially-complete -> complete
                   -> failed -> retrying -> complete
```

State transitions should be validated and auditable. Do not use a state-machine library for a trivial two-state flag.

### Idempotency

Scheduled jobs, webhooks, imports, deliveries, migrations, and retries should have an idempotency strategy when duplicate execution is possible. Define the logical operation key and expected behavior on repeat.

### Locking and concurrency

Use a clear overlap policy for scheduled work:

- prevent overlap;
- partition safely;
- or make overlap correct.

Test race-prone paths with reasoning and targeted validation; a passing happy-path test does not prove concurrency safety.

### Transactional outbox

Use an outbox only when a database state change and asynchronous message must be made reliably together. Do not introduce it in a single-process workflow that has no such atomicity problem.

### Retry with bounded failure

Retries need:

- classified retryable errors;
- bounded attempts/time;
- backoff and jitter when appropriate;
- idempotency;
- visibility and dead-letter/recovery behavior;
- protection against retry storms.

### Reconciliation

Managed services should be able to reconcile expected versus actual work. For data collection and delivery this may include run counts, item counts, file checksums, missing records, and source-to-output traceability.

## 8. Data and contract design

- Treat schemas, API formats, and client files as versioned contracts.
- Validate at system boundaries.
- Prefer explicit units, currencies, time zones, identifiers, and null semantics.
- Preserve raw evidence separately from normalized interpretation where auditability matters.
- Make migrations forward-testable and recoverable.
- Avoid dual sources of truth for mutable business configuration.
- Use tenant/client identifiers in authorization and data-access tests, not only UI filtering.

## 9. Error handling and observability

A robust design defines:

- which failures are expected;
- what is retried;
- what is surfaced to users/operators;
- what state remains after partial failure;
- how a run or request is correlated across components;
- what is logged without exposing secrets or client data;
- how missing work is detected;
- how recovery is performed.

Do not catch broad exceptions only to log and continue as though work succeeded.

## 10. Testing strategy

Use the smallest test level that provides credible evidence, with higher-level coverage for important seams.

| Test type | Purpose |
|---|---|
| unit/property | deterministic policy, calculations, validation, boundaries |
| contract | adapters, schemas, interchangeable implementations, client outputs |
| integration | database, filesystem, queue, external-service boundary using safe environment |
| smoke/end-to-end | critical user/operational path |
| characterization | preserve poorly documented existing behavior before refactor |
| migration/recovery | schema progression, backup/restore, retry, rollback/forward recovery |

Tests should fail when the behavior is broken. More tests are not automatically better; duplicate or implementation-coupled tests create maintenance debt.

## 11. Pattern admission questions

Before introducing a pattern, framework, or abstraction, answer:

1. What current problem does it solve?
2. What concrete consumers or variations exist now?
3. What simpler existing mechanism was considered?
4. What new files, dependencies, runtime services, and failure modes does it add?
5. How will it be tested and operated?
6. How can it be removed or changed later?
7. Does it improve the whole system or only make one class diagram look cleaner?

If the answers are weak, implement the direct solution and revisit when evidence appears.

## 12. Review checklist

A design review should ask:

- Does this belong in the current system?
- Is the execution path understandable?
- Are boundaries aligned to actual change and risk?
- Is any abstraction speculative?
- Are security and data-isolation checks at the correct boundary?
- Are failures, retries, and partial states explicit?
- Are data and API contracts versioned and tested?
- Can the change be rolled back or safely recovered?
- Are tests at the right levels?
- Is there a simpler solution using the existing stack?
- Does the change improve repository health rather than merely move complexity?

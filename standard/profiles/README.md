# Repository Profiles

Profiles standardize the parts of source layout that genuinely differ by project topology. Every repository selects one primary profile in `.repo-standard.json`; secondary profiles are added only when they materially change structure or validation.

| Profile | Select when |
|---|---|
| [`single-application.md`](single-application.md) | One deployable application or modular monolith |
| [`monorepo.md`](monorepo.md) | Multiple intentional applications/packages share one repository |
| [`data-platform.md`](data-platform.md) | Collection, ingestion, transformation, analytics, or ML workflows dominate |
| [`infrastructure.md`](infrastructure.md) | Infrastructure-as-code, policies, and environment composition dominate |

Profiles are guidance, not permission to mass-move an existing repository. During bootstrap, preserve established framework-native paths and record equivalent mappings in `.repo-standard.json`. Structural convergence requires a separate behavior-preserving refactor plan.

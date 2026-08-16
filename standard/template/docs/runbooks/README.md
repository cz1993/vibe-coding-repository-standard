# Runbooks

**Status:** Authoritative  
**Owner:** Replace with operations owner  
**Last validated:** 2026-08-15  
**Validated by:** Replace with rehearsal or operational evidence

A runbook is a human-executable operational procedure. Create one only for a real event or recurring operation.

Each runbook should include:

```text
Purpose and trigger
Owner/escalation
Environment and permission requirements
Preconditions and safety checks
Exact verified steps
Expected evidence after each critical step
Failure/abort conditions
Rollback or forward recovery
Validation and reconciliation
Sensitive-data/logging rules
Last safe rehearsal date
```

Do not place secret values in runbooks. Link to the approved secret-management location and use variable names or references.

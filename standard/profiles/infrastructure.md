# Profile: Infrastructure

## Select when

The repository primarily defines infrastructure-as-code, cloud/platform configuration, policy-as-code, networking, identity, CI/CD infrastructure, or environment composition.

## Recommended shape

```text
modules/                 # reusable infrastructure modules
environments/            # composition and references, never secret values
policies/                 # policy-as-code
scripts/                  # thin operator commands
tests/                    # static, policy, plan, and safe integration tests
docs/
```

## Rules

- Never commit secret values, private keys, state containing secrets, or production exports.
- Environment directories compose versioned modules; avoid copying modules between environments.
- Plans and generated provider output are evidence, not permanent source unless explicitly sanitized and retained.
- Separate read/plan from apply/destroy permissions.
- Production apply, migration, deletion, DNS, identity, and network changes require explicit approval and rollback/forward-recovery evidence.
- Pin and update provider/module versions deliberately.
- Use policy and static validation before live changes.

## Expected evidence

- format/validate/lint/policy commands;
- safe plan output and reviewed change set;
- environment and account/subscription targeting controls;
- state/backend ownership and recovery;
- least-privilege role definitions;
- deployment/apply and rollback runbooks;
- drift detection and audit logging.

## Anti-patterns

- shared credentials in local/global agent context;
- one script that can silently plan and apply;
- duplicated environment definitions;
- unrestricted production MCP/cloud tools in ordinary development profiles;
- agents allowed to self-approve destructive operations.

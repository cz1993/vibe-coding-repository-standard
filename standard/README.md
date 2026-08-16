# VCRS standard library

This directory contains the reusable standard behind the public VCRS project. Start with the path that matches your goal.

| Goal | Start here |
|---|---|
| Understand the design and requirements | [`handbook/README.md`](handbook/README.md) |
| Select a repository topology | [`profiles/README.md`](profiles/README.md) |
| Run a Codex workflow | [`prompts/README.md`](prompts/README.md) |
| Configure a conservative machine profile | [`machine-profile/README.md`](machine-profile/README.md) |
| Adapt the starter files to a repository | [`template/README.md`](template/README.md) |

The directories are related but intentionally separate:

- the **handbook** explains decisions and defines the standard;
- **profiles** adapt the standard to different repository topologies;
- **prompts** turn the guidance into bounded execution workflows;
- the **machine profile** keeps global Codex context small and project-neutral;
- the **template** provides files and validators to adapt, not blindly overwrite.

For the beginner path, return to the [15-minute getting-started guide](../docs/getting-started.md).

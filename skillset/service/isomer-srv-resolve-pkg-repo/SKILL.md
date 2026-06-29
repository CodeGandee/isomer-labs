---
name: isomer-srv-resolve-pkg-repo
description: Use when an Isomer Labs agent must choose or fall back to package repositories or channels for package managers such as pixi, uv, conda, pip, npm, bun, pnpm, or cargo, especially behind slow or blocked networks, when mirror configuration is suspected, or when NVIDIA packages need channel prioritization.
---

# Isomer Service Resolve Package Repository

## Overview

Choose reachable, policy-aligned package repositories and channels before installing dependencies. Prefer official upstream sources, fall back to user-declared mirrors from local package-manager configuration, and report a blocker only when no usable source can be reached.

## When to Use

Use this skill when a task requires selecting a package repository before installation and any of the following is true:

- The environment may block or slow the official upstream source.
- A local mirror or private registry is likely configured.
- NVIDIA/CUDA packages are involved and the `nvidia` channel may be preferable to `conda-forge`.
- The user explicitly asks which channel, registry, or index to use.

Do not use this skill when the repository is already fixed by a Service Request, environment gate, or manifest and no reachability concern exists.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Identify the package manager** named in the task or implied by the manifest, lockfile, or command. See **Supported Package Managers**.
2. **Select one subcommand** from the **Subcommands** table:
   - If the prompt describes repository resolution but does not name a subcommand, use `pixi-resolve` when Pixi is involved.
3. **Load the selected reference page** and resolve its required inputs.
4. **Execute the selected subcommand's workflow** to determine the recommended repository, mirror, or channel list.
5. **Record the resolution** in the active environment gate, manifest comment, or command log:
   - Include the reachability test, the source of any mirror, and any NVIDIA channel preference applied.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the subcommands and constraints in this skill, then execute the plan.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `pixi-resolve` | Resolve reachable Conda channels for Pixi, with NVIDIA channel preference | [references/pixi-resolve.md](references/pixi-resolve.md) |
| `uv-resolve` | Resolve reachable Python package indexes for uv | [references/uv-resolve.md](references/uv-resolve.md) |
| `conda-resolve` | Resolve reachable channels for Conda | [references/conda-resolve.md](references/conda-resolve.md) |
| `pip-resolve` | Resolve reachable Python package indexes for pip | [references/pip-resolve.md](references/pip-resolve.md) |
| `npm-resolve` | Resolve reachable registries for npm | [references/npm-resolve.md](references/npm-resolve.md) |
| `bun-resolve` | Resolve reachable registries for Bun | [references/bun-resolve.md](references/bun-resolve.md) |
| `help` | Explain this skill and list public subcommands | This entrypoint |

## Supported Package Managers

The skill currently covers pixi, uv, conda, pip, npm, and bun. Other package managers may be added later. For an unsupported manager, apply the same pattern: test the official upstream, inspect local user configuration for mirrors, test each candidate, prefer vendor channels for vendor packages, and stop with a blocker when nothing is reachable.

## Common Mistakes

- **Assuming the official source is reachable**. Always test reachability before depending on it; many environments block or rate-limit upstream sources.
- **Ignoring user mirror config**. Local `~/.condarc`, `~/.pip/pip.conf`, `~/.npmrc`, and `bunfig.toml` are authoritative evidence of intended mirrors.
- **Forgetting NVIDIA channel preference**. For NVIDIA packages on Conda/Pixi, prefer the `nvidia` channel over `conda-forge` when both are reachable.
- **Recording only the winner**. Note every candidate tested, why it was rejected, and the source of the chosen mirror so the decision remains auditable.
- **Mutating manifests before confirming reachability**. Resolve repositories first; do not run install commands against a source that has not been tested.

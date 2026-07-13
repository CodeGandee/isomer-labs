---
name: isomer-dev-testing
description: Use when the user explicitly asks to install or refresh the current Isomer Labs checkout as an editable user-space uv tool with a commit-stamped local build version for development or CLI testing.
---

# Isomer Development Testing

## Overview

Use this skill for development-only installation and verification procedures that expose the current Isomer Labs source checkout through user-space tooling. Keep local version stamping temporary in the source tree and preserve every pre-existing worktree change.

## When to Use

Use this skill when the user wants the current checkout installed through `uv tool`, wants `isomer-cli` to reflect source edits without reinstallation, or needs a commit-identifiable local build for CLI testing.

Do not use it for PyPI releases, isolated Pixi environment setup, system-wide installation, or packaged system-skill installation. Route those requests to their owning release, environment, or system-skill workflow.

## Workflow

1. **Select the subcommand** from the **Subcommands** table. If no actionable subcommand is present, show the available subcommands without mutating the checkout or user tool directory.
2. **Resolve the Isomer Labs checkout** from the user-supplied path or current directory. Require its `pyproject.toml`, Git metadata, and `isomer-cli` project script before proceeding.
3. **Load the subcommand page** and follow its workflow, including its restoration and verification gates.
4. **Report the result** with the installed local version, editable source path, executable path, uv receipt evidence, and worktree-preservation result.

If the request does not map cleanly to these steps, use the native planning tool to build and execute a bounded plan from the constraints in this skill without broadening the requested installation scope.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `install-to-uv` | Install or refresh the current Isomer Labs checkout as an editable user-space uv tool after temporarily applying a commit-stamped PEP 440 local version. | [commands/install-to-uv.md](commands/install-to-uv.md) |

## Common Mistakes

- Leaving the local version in `pyproject.toml` after installation. Restore the exact original version on success and failure.
- Using `uv pip install --system`, `pip install --user`, or `sudo`. This procedure owns a user-space `uv tool` installation.
- Installing a directory without `--editable`. Verify both the uv receipt and `direct_url.json` instead of inferring editability from the source URL.
- Cleaning or resetting a dirty checkout. Preserve user changes and compare the final worktree state with the captured preflight state.
- Reporting only the project release version. The installed tool must report the generated `+local.<commit>` version.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.

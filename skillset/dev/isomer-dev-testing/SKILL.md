---
name: isomer-dev-testing
description: Use when the user explicitly asks to install or refresh the current Isomer Labs checkout as an editable user-space uv tool with a commit-stamped local build version, or to project packaged Isomer system skills and preserve, refresh, add, or explicitly remove skillset/dev/ development skills in local AI coding tool skill roots for development or CLI testing.
---

# Isomer Development Testing

## Overview

Use this skill for development-only installation and verification procedures that expose the current Isomer Labs source checkout through user-space tooling. Keep local version stamping temporary in the source tree and preserve every pre-existing worktree change.

## When to Use

Use this skill when the user wants the current checkout installed through `uv tool`, wants `isomer-cli` to reflect source edits without reinstallation, needs a commit-identifiable local build for CLI testing, or wants packaged Isomer system skills (and optionally `skillset/dev/` development skills) projected into local AI coding tool directories such as `.agents/`, `.claude/`, `.codex/`, or `.kimi-code/`.

Do not use it for PyPI releases, isolated Pixi environment setup, or system-wide installation. Route those requests to their owning release or environment workflow.

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
| `install-isomer-skills` | Project packaged Isomer system skills into local AI coding tool skill roots, preserve and refresh existing `skillset/dev/` development skills, add named development skills, and remove development skills only when explicitly requested. | [commands/install-isomer-skills.md](commands/install-isomer-skills.md) |

## Guardrails

- DO NOT use this skill for PyPI releases, system-wide installation, or isolated Pixi environment setup.
- DO NOT leave a temporary commit-stamped local version in `pyproject.toml` after `install-to-uv`.
- DO NOT use `uv pip install --system`, `pip install --user`, `sudo`, or non-editable installation for `install-to-uv`.
- DO NOT clean or reset a dirty checkout to make `install-to-uv` verification pass.
- DO NOT install packaged extensions or `--all-extensions` unless the user explicitly names them.
- DO NOT add a new `skillset/dev/` development skill unless the user explicitly names it, but preserve and refresh development skills that already exist in a selected tool skill root.
- DO NOT remove an existing development skill merely because the current request does not name it. Remove one only when the user explicitly asks to remove or uninstall that skill.
- DO NOT replace a real skill directory with a symlink or copy without first confirming the user.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.

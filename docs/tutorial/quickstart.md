# Quickstart

This tutorial creates and validates a local Isomer Project.

## Install the CLI

Install the released package with uv:

```bash
uv tool install isomer-labs
isomer-cli --help
```

When working from a source checkout, use the developer setup in [Testing](../developer/testing.md). The rest of this tutorial assumes the released CLI is installed and available as `isomer-cli`.

## Install System Skills

Install the packaged core skills into the coding-agent surface you use. Pick one target, or use `all` when you intentionally want every supported target populated. This quickstart uses user scope so the skills remain available after you create and enter the Project directory; use project scope from an existing project directory when you want a local installation.

List optional agent-skill extensions or inspect one extension before installation:

```bash
isomer-cli system-skills extensions list
isomer-cli system-skills extensions show kaoju
```

```bash
isomer-cli system-skills install --target codex --scope user
isomer-cli system-skills install --target claude-code --scope user
isomer-cli system-skills install --target kimi-code --scope user
isomer-cli system-skills install --target generic --scope user
```

Every install, status, upgrade, and uninstall command requires `--scope user|project`.

| Target | Project Scope | User Scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

Use `--extension deepsci` when the agent should run the DeepSci research workflow skills:

```bash
isomer-cli system-skills install --target codex --scope user --extension deepsci
```

Use `--extension kaoju` when the agent should survey literature and codebases or perform first-hand method trials and comparisons. Invoke it through `$isomer-kaoju-pipeline` after installation.

```bash
isomer-cli system-skills install --target codex --scope user --extension kaoju
```

The pipeline routes ten user intents from direction selection and reading-list construction through source ingestion, MyST paper production, package-owned wiki export, environment preparation, and separately approved code trials. Users and agents acquire repositories with fit-for-purpose commands outside Isomer, verify the selected source and immutable identity, then use `project repos register` and `project artifacts` for topology and durable provenance. Other deterministic state operations use `project runs`, `project service-requests`, `ext kaoju paper`, and `ext kaoju wiki`; the installed skills decide what research work those services should perform.

## Create a Project

Create a directory that will own the project manifest, topic workspaces, runtime files, and GUI-readable records:

```bash
mkdir my-isomer-project
cd my-isomer-project
isomer-cli project init
```

Validate the directory before adding topic work:

```bash
isomer-cli --print-json project validate
```

## Next Steps

- Continue to [Author Research Intent](author-research-intent.md) when you are ready to create a Research Topic.
- Read [Concepts](../manual/concepts.md) before naming new domain objects.
- Use [CLI Reference](../manual/cli-reference.md) when you need command flags or JSON output shape.

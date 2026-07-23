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

Install the packaged core pack into the coding-agent surface you use. The host discovers two public siblings: `isomer-op-welcome` teaches typical workflows without mutating the Project, and `isomer-op-entrypoint` routes concrete work to its 20 protected capabilities. Pick one target, or use `all` when you intentionally want every supported target populated. This quickstart uses user scope so the pack remains available after you create and enter the Project directory; use project scope from an existing project directory when you want a local installation.

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

From an existing Project directory, omit scope for a Project-local installation:

```bash
isomer-cli system-skills install --target codex
```

When `--scope` is omitted, `system-skills install` defaults to Project scope at the exact current working directory and does not search ancestor Git or Isomer roots. Explicit `--scope project` is equivalent, while `--scope user` is the only route to user-wide installation. `system-skills status`, `upgrade`, and `uninstall` require an explicit `--scope user|project`.

| Target | Project Scope | User Scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

Use `--extension deepsci` when the agent should run DeepSci. This installs core plus the complete DeepSci pack: the public `isomer-ext-deepsci-welcome` and `isomer-ext-deepsci-entrypoint` siblings and their 21 protected members.

```bash
isomer-cli system-skills install --target codex --scope user --extension deepsci
```

Use `--extension kaoju` when the agent should survey literature and codebases or perform first-hand method trials and comparisons. This installs core plus the complete Kaoju pack: the public `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` siblings and their 13 protected members.

```bash
isomer-cli system-skills install --target codex --scope user --extension kaoju
```

Refresh the coding-agent host or start a new session after installation. Start with the public welcome skill when you need orientation, then invoke the corresponding public entrypoint for concrete work:

```text
$isomer-op-welcome
$isomer-op-welcome show-command-map
$isomer-ext-deepsci-welcome show-options
$isomer-ext-kaoju-welcome show-command-map
$isomer-op-entrypoint use help to show the compatibility welcome handoff
$isomer-ext-deepsci-entrypoint use empirical-pass to test a selected hypothesis
$isomer-ext-kaoju-entrypoint use build-reading-list to collect survey evidence
```

Protected members are parent-routed capabilities, not separate public skills. Their nested files are readable as part of the pack; protected is a discovery and routing classification, not an access-control boundary.

The pipeline routes ten user intents from direction selection and reading-list construction through source ingestion, MyST paper production, package-owned wiki export, environment preparation, and separately approved code trials. Users and agents acquire repositories with fit-for-purpose commands outside Isomer, verify the selected source and immutable identity, then use `project repos register` and `project artifacts` for topology and durable provenance. Other deterministic state operations use `project runs`, `project service-requests`, `ext kaoju paper`, and `ext kaoju wiki`; the installed skills decide what research work those services should perform.

If a concrete research target lacks an input that an installed skill can produce, an ordinary request pauses before prerequisite mutation and presents recovery choices. You may explicitly tell the agent to run to the target, which authorizes routine in-scope prerequisites and the target for that prompt only. This is not an `isomer-cli` command, global yes-to-all flag, Project setting, or Run-level Control Mode. The agent preserves each owner Run and Gate, pauses at protected human or external-side-effect boundaries, and stops after the named target.

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

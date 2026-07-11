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

Install the packaged core skills into the coding-agent surface you use. Pick one target, or use `all` when you intentionally want every supported local target populated.

List optional agent-skill extensions or inspect one extension before installation:

```bash
isomer-cli system-skills extensions list
isomer-cli system-skills extensions show kaoju
```

```bash
isomer-cli system-skills install --target codex
isomer-cli system-skills install --target claude-code
isomer-cli system-skills install --target kimi-code
isomer-cli system-skills install --target generic
```

Use `--extension deepsci` when the agent should run the DeepSci research workflow skills:

```bash
isomer-cli system-skills install --target codex --extension deepsci
```

Use `--extension kaoju` when the agent should survey literature and codebases or perform first-hand method trials and comparisons. Invoke it through `$isomer-kaoju-pipeline` after installation.

```bash
isomer-cli system-skills install --target codex --extension kaoju
```

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

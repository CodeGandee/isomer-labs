# Quickstart

This tutorial creates and validates a local Isomer Project.

## Install the CLI

Install the released package with uv:

```bash
uv tool install isomer-labs
isomer-cli --help
```

When working from a source checkout, use the developer setup in [Testing](../developer/testing.md). The rest of this tutorial assumes the released CLI is installed and available as `isomer-cli`.

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

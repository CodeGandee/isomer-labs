# Quickstart

This tutorial creates a local Isomer Project, adds one Research Topic, validates the project, and opens the GUI.

## Install the CLI

Install the released package with uv:

```bash
uv tool install isomer-labs
isomer-cli --help
```

When working from a source checkout, run the CLI through Pixi instead:

```bash
pixi install
pixi run isomer-cli --help
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

## Create a Research Topic

Add one topic and make it the default topic for commands that accept `--topic`:

```bash
isomer-cli project topics create flash-attention-runtime \
  --statement "Model FlashAttention host and GPU runtime behavior." \
  --set-default
```

Inspect the created topic paths:

```bash
isomer-cli --print-json project paths list --topic flash-attention-runtime
```

## Open the GUI

Start the single-user web service from the project root:

```bash
isomer-cli project web serve --root .
```

Open the printed URL. The topic overview page reads `intent/src/topic-overview.md` from the selected Topic Workspace and the JSON payloads from the record index.

## Next Steps

- Read [Concepts](../manual/concepts.md) before naming new domain objects.
- Use [CLI Reference](../manual/cli-reference.md) when you need command flags or JSON output shape.
- Follow [Install System Skills](system-skills.md) when you want an agent to use the Isomer workflows.

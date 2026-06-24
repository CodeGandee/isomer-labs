# Getting Started

This guide shows the smallest useful path from an empty directory to a recorded Agent Team Instance. Every step is explicit about whether it reads state or mutates Project files, Workspace Runtime records, or adapter material.

## Prerequisites

- Python 3.11 or later.
- Pixi installed and available on `PATH`.
- The `isomer-labs` package installed in editable mode through Pixi.
- A resolvable Houmao CLI boundary for Project bootstrap: `houmao-mgr` on `PATH`, `ISOMER_HOUMAO_COMMAND`, or a local checkout that Isomer can find.

Run `pixi install` from the repository root to resolve dependencies and make `isomer-cli` available.

## Initialize a Project

`isomer-cli project init` creates the smallest valid Isomer-managed Project. It initializes the Project-level Houmao overlay (`.houmao/`) through the supported Houmao CLI boundary, then writes the Project Config Directory (`.isomer-labs/`), the Project Manifest (`manifest.toml`), a Research Topic Config, the selected generated content root (`isomer-content/` by default), and a Topic Workspace directory.

```bash
pixi run isomer-cli project init
```

By default the command creates a Research Topic named `default` and a Topic Workspace named `default` under `isomer-content/topic-ws/default/`. You can name the topic explicitly:

```bash
pixi run isomer-cli project init my-topic
```

You can choose a different project-local generated content root at initialization time. In that case, the Topic Workspace base is derived from the selected root:

```bash
pixi run isomer-cli project init my-topic --content-dir custom-content
```

This creates the Topic Workspace under `custom-content/topic-ws/my-topic/` and records `custom-content` plus `custom-content/topic-ws` in `.isomer-labs/manifest.toml`.

This command mutates the Project filesystem. It does not create `state.sqlite`, Workspace Runtime subdirectories, Agent Workspaces, adapter launch material, mailboxes, gateways, managed agents, sessions, or launch dossiers.

The selected content root's generated `.gitignore` ignores generated content by default and keeps only `README.md` and `.gitignore` unignored. Track selected generated files only when you intentionally want them in Git.

## Validate the Project

`isomer-cli project validate` checks the Project Manifest and registered Research Topic Configs. It is read-only.

```bash
pixi run isomer-cli --print-json project validate
```

Use `isomer-cli project doctor` to check host Pixi availability, Project-level Pixi configuration, and Research Topic environment bindings. It is also read-only.

```bash
pixi run isomer-cli --print-json project doctor
```

## Inspect Context and Paths

Before creating runtime state, resolve the Effective Topic Context and preview filesystem paths.

```bash
pixi run isomer-cli --print-json project context show --topic default
pixi run isomer-cli project paths preview --topic default
```

Both commands are read-only. `project context show` displays the resolved Project, Research Topic, Topic Workspace, and selected refs for a topic-scoped command. `project paths preview` prints the generated content root and path plan without creating directories.

## Initialize and Prepare Workspace Runtime

`isomer-cli project runtime init` creates or reopens the Workspace Runtime for the selected Topic Workspace. It creates `state.sqlite`, records schema metadata, and creates the default runtime directories (`artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, `logs/`).

```bash
pixi run isomer-cli --print-json project runtime init --topic default
```

`isomer-cli project runtime prepare` records Topic Environment Readiness. It checks only explicit Project Manifest bindings (`topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings`) and records `ready`, `failed`, or `blocked` status. It does not install Pixi environments implicitly.

```bash
pixi run isomer-cli --print-json project runtime prepare --topic default
```

If readiness is `failed` or `blocked`, repair is explicit. Treat environment setup or compatibility work as a Service Request rather than hiding it inside `project runtime prepare`.

## Validate Readiness

```bash
pixi run isomer-cli --print-json project runtime validate --topic default --require-ready-readiness
```

This command is read-only and reports launch-facing errors when readiness is not `ready`.

## Create an Agent Team Instance Record

An Agent Team Instance is a concrete runtime team created from a Topic Agent Team Profile. The `project team-instances create` command writes Agent Instance records, Agent Workspace records, path plans, initial Workflow Stage Cursor records, and provenance refs, and it materializes Agent Workspace directories. It does not launch Houmao agents or write adapter-specific launch material.

```bash
pixi run isomer-cli --print-json project team-instances create \
  --topic default \
  --id ati-default-deepsci
```

You can list and inspect the record:

```bash
pixi run isomer-cli project team-instances list --topic default
pixi run isomer-cli --print-json project team-instances show ati-default-deepsci --topic default
```

At this point the Project has a durable Agent Team Instance record but no live agents. To launch through the Houmao adapter, see [Houmao Adapter](houmao-adapter.md) and [Workflows](workflows.md).

## Next Steps

- Read [Concepts](concepts.md) for a concise overview of the domain model.
- Read [System Design](system-design.md) to understand how discovery, context, paths, and runtime fit together.
- Read [isomer-cli Reference](isomer-cli.md) for every public command.
- Read [Workflows](workflows.md) for operator-oriented paths including quick launch and prepare-only operation.

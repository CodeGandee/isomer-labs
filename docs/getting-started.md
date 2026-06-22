# Getting Started

This guide shows the smallest useful path from an empty directory to a recorded Agent Team Instance. Every step is explicit about whether it reads state or mutates Project files, Workspace Runtime records, or adapter material.

## Prerequisites

- Python 3.11 or later.
- Pixi installed and available on `PATH`.
- The `isomer-labs` package installed in editable mode through Pixi.

Run `pixi install` from the repository root to resolve dependencies and make `isomer-cli` available.

## Initialize a Project

`isomer-cli init` creates the smallest valid Isomer-managed Project. It writes the Project Config Directory (`.isomer-labs/`), the Project Manifest (`manifest.toml`), a Research Topic Config, and a Topic Workspace directory.

```bash
pixi run isomer-cli init
```

By default the command creates a Research Topic named `default` and a Topic Workspace named `default` under `topic-workspaces/default/`. You can name the topic explicitly:

```bash
pixi run isomer-cli init my-topic
```

This command mutates the Project filesystem. It does not create `state.sqlite`, Workspace Runtime subdirectories, Agent Workspaces, or adapter launch material.

## Validate the Project

`isomer-cli validate` checks the Project Manifest and registered Research Topic Configs. It is read-only.

```bash
pixi run isomer-cli --print-json validate
```

Use `isomer-cli doctor` to check host Pixi availability, Project-level Pixi configuration, and Research Topic environment bindings. It is also read-only.

```bash
pixi run isomer-cli --print-json doctor
```

## Inspect Context and Paths

Before creating runtime state, resolve the Effective Topic Context and preview filesystem paths.

```bash
pixi run isomer-cli --print-json context show --topic default
pixi run isomer-cli paths preview --topic default
```

Both commands are read-only. `context show` displays the resolved Project, Research Topic, Topic Workspace, and selected refs for a topic-scoped command. `paths preview` prints the path plan without creating directories.

## Initialize and Prepare Workspace Runtime

`isomer-cli runtime init` creates or reopens the Workspace Runtime for the selected Topic Workspace. It creates `state.sqlite`, records schema metadata, and creates the default runtime directories (`artifacts/`, `agents/`, `tasks/`, `runs/`, `views/`, `logs/`).

```bash
pixi run isomer-cli --print-json runtime init --topic default
```

`isomer-cli runtime prepare` records Topic Environment Readiness. It checks only explicit Project Manifest bindings (`topic_pixi_environment_bindings` and `topic_standalone_pixi_bindings`) and records `ready`, `failed`, or `blocked` status. It does not install Pixi environments implicitly.

```bash
pixi run isomer-cli --print-json runtime prepare --topic default
```

If readiness is `failed` or `blocked`, repair is explicit. Treat environment setup or compatibility work as a Service Request rather than hiding it inside `runtime prepare`.

## Validate Readiness

```bash
pixi run isomer-cli --print-json runtime validate --topic default --require-ready-readiness
```

This command is read-only and reports launch-facing errors when readiness is not `ready`.

## Create an Agent Team Instance Record

An Agent Team Instance is a concrete runtime team created from a Topic Agent Team Profile. The `team-instances create` command writes Agent Instance records, Agent Workspace records, path plans, initial Workflow Stage Cursor records, and provenance refs, and it materializes Agent Workspace directories. It does not launch Houmao agents or write adapter-specific launch material.

```bash
pixi run isomer-cli --print-json team-instances create \
  --topic default \
  --topic-agent-team-profile default-deepsci \
  --id ati-default-deepsci
```

You can list and inspect the record:

```bash
pixi run isomer-cli team-instances list --topic default
pixi run isomer-cli --print-json team-instances show ati-default-deepsci --topic default
```

At this point the Project has a durable Agent Team Instance record but no live agents. To launch through the Houmao adapter, see [Houmao Adapter](houmao-adapter.md) and [Workflows](workflows.md).

## Next Steps

- Read [Concepts](concepts.md) for a concise overview of the domain model.
- Read [System Design](system-design.md) to understand how discovery, context, paths, and runtime fit together.
- Read [isomer-cli Reference](isomer-cli.md) for every public command.
- Read [Workflows](workflows.md) for operator-oriented paths including quick launch and prepare-only operation.

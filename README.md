# isomer-labs

Isomer Labs is a research workbench for running multi-agent research topics from a project directory. It gives operators a CLI, packaged system skills, topic workspaces, durable records, and a local web GUI for inspecting how ideas, experiments, and artifacts evolve.

## Install

Install the CLI as a uv tool:

```bash
uv tool install isomer-labs
isomer-cli --help
```

For development from a checkout, use Pixi:

```bash
pixi install
pixi run isomer-cli --help
```

## Start a Project

```bash
mkdir my-isomer-project
cd my-isomer-project
isomer-cli project init
isomer-cli project topics create my-topic --statement "Investigate the concrete research question." --set-default
isomer-cli --print-json project validate
```

Start the local GUI over the project directory:

```bash
isomer-cli project web serve --root .
```

Then open the printed local URL and choose the Research Topic to inspect.

## Install System Skills

Install packaged Isomer skills with `npx skills add`. The entrypoint skill is the best starting point for operators because it routes known tasks to the right Isomer skill or CLI command.

```bash
npx skills add https://github.com/CodeGandee/isomer-labs/tree/main/src/isomer_labs/assets/system_skills/operator/isomer-op-entrypoint --agent codex --yes
```

Install the welcome skill when you want an agent to bootstrap a first-time Project Operator Session:

```bash
npx skills add https://github.com/CodeGandee/isomer-labs/tree/main/src/isomer_labs/assets/system_skills/operator/isomer-op-welcome --agent codex --yes
```

Install extension skills the same way when a project needs them, for example the DeepSci pipeline skill:

```bash
npx skills add https://github.com/CodeGandee/isomer-labs/tree/main/src/isomer_labs/assets/system_skills/research-paradigm/deepsci/isomer-deepsci-pipeline --agent codex --yes
```

## Documentation

- [Documentation Home](docs/index.md)
- [Quickstart](docs/tutorial/quickstart.md)
- [CLI Reference](docs/manual/cli-reference.md)
- [Concepts](docs/manual/concepts.md)
- [Developer Guide](docs/developer/index.md)

## Status

The project is early but usable for local research-project setup, topic workspace management, record indexing, and GUI inspection. See [Assumptions and Roadmap](docs/developer/assumptions-and-roadmap.md) for current boundaries.

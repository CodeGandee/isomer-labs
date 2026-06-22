# isomer-labs

艾索幕实验室

Isomer Labs is a private research platform that uses multi-agent teams as a research engine while a human operator sets goals and steers work at critical steps.

The same base capabilities can form different research teams, workflows, and feedback loops. One Research Topic may need discovery, synthesis, and review agents; another may need planning, data analysis, and report-writing agents. The platform makes those structures easy to create, run, observe, and improve.

## Documentation

- [Getting Started](docs/getting-started.md) — initialize a Project, validate it, prepare a Topic Workspace, and create an Agent Team Instance record.
- [isomer-cli Reference](docs/isomer-cli.md) — every public command, its side effects, and common examples.
- [Documentation Index](docs/index.md) — all docs pages and navigation.

## Quick Sampler

```bash
pixi install
pixi run isomer-cli init
pixi run isomer-cli --print-json validate
pixi run isomer-cli --print-json runtime init --topic default
pixi run isomer-cli --print-json runtime prepare --topic default
pixi run isomer-cli --print-json team-instances create \
  --topic default \
  --topic-agent-team-profile default-deepsci \
  --id ati-default-deepsci
```

For Houmao-backed launch paths, see [docs/workflows.md](docs/workflows.md) and [docs/houmao-adapter.md](docs/houmao-adapter.md).

## Status

Initial sketch. Structure and scope are expected to change. See [Assumptions and Roadmap](docs/assumptions-and-roadmap.md) for current milestone status and future work.

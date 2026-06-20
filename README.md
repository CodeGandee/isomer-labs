# isomer-labs

艾索幕实验室

## Sketch

Isomer Labs is a private lab for developing an automatic research platform powered by multi-agent technology.

## Project Goal

Isomer Labs aims to develop an interactive, semi-automatic research conduction platform. The platform uses multi-agent research teams as a research engine, while a human user sets goals and steers the work at critical steps.

The project is inspired by DeepScientist, available locally under `extern/orphan/DeepScientist`, but it differs in several design goals:

- support multi-agent teamwork from the start, including predefined research teams and user-defined agent teams
- keep agent-team composition open to customization as a core platform capability
- expose a modular, white-box system rather than a fully system-controlled workflow
- decouple the research engine from the GUI
- drive the research engine through an operator agent controlled by the user
- generate task-specific GUI views for visualizing research artifacts
- organize projects so they can integrate into user-owned workspaces

## Name

`Isomer Labs` reflects the platform's core idea: research work can be reorganized into different agent structures depending on the problem.

The same base capabilities can form different research teams, workflows, and feedback loops. One task may need discovery, synthesis, and review agents; another may need planning, data analysis, and report-writing agents. The platform should make those structures easy to create, run, observe, and improve.

The name points to that adaptive structure: a research system that changes shape around the question while staying coherent as one platform.

The repository starts intentionally light:

- collect platform ideas before they become product features
- sketch multi-agent research workflows and interfaces
- keep experiments private until they are ready to split out

## External References

Local-only external checkouts live under `extern/orphan/` and are not committed.
The current reference package is:

- `DeepScientist`: cloned from `https://github.com/ResearAI/DeepScientist` into
  `extern/orphan/DeepScientist` with `--depth=1`.

## Milestone 1 CLI

The package exposes `isomer-cli` for Project discovery, Project Manifest validation, Effective Topic Context inspection, and side-effect-free Workspace Path Resolution previews.

Common examples:

```bash
pixi run isomer-cli init
pixi run isomer-cli validate --json
pixi run isomer-cli topics list
pixi run isomer-cli workspaces list
pixi run isomer-cli context show --topic default --json
pixi run isomer-cli paths preview --topic default
pixi run isomer-cli schemas list
```

`isomer-cli init` creates `.isomer-labs/manifest.toml`, `.isomer-labs/research-topics/default.toml`, and `topic-workspaces/default/`. It does not create `state.sqlite` or Workspace Runtime subdirectories.

## Status

Initial sketch. Structure and scope are expected to change.

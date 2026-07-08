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

## Topic Workspace Explained

An Isomer Project can contain many Research Topics. Each topic gets its own Topic Workspace, usually under `isomer-content/topic-ws/<topic-id>/`, and that workspace is the topic's storage and execution boundary.

The Topic Workspace owns the topic Pixi environment. Dependencies for research code, profiling scripts, renderers, and validation tools should be added to the Topic Workspace `pixi.toml`, not silently installed into the Project root or the user's global Python. This keeps one topic's runtime requirements from leaking into another topic.

The Topic Workspace also owns the research storage layout:

- `intent/` stores the topic overview, environment gate, actor definitions, and derived setup gates.
- `records/` stores durable research records, artifacts, evidence items, decisions, view manifests, and the SQLite index used by the GUI.
- `runtime/` stores Workspace Runtime state, adapter payloads, launch material, and resumable execution state.
- `repos/topic-main/` is the topic-owned development repository for code-bearing work.
- `repos/extern/` stores canonical external repositories such as upstream source checkouts.
- `actors/` and `agents/` store actor or agent workspaces, usually as worktrees of `repos/topic-main`.

The Project Manifest records where each Topic Workspace lives, while `topic-workspace.toml` inside the workspace binds semantic labels such as `topic.repos.main`, `topic.records`, and `topic.runtime` to concrete paths. Agents and skills should resolve those labels instead of guessing paths.

## Install System Skills

Install packaged Isomer skills with `isomer-cli system-skills install`. The entrypoint skill is included in the core group and is the best starting point for operators because it routes known tasks to the right Isomer skill or CLI command.

```bash
isomer-cli system-skills install --target codex
```

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`. `codex` installs to `$CODEX_HOME/skills` or `~/.codex/skills`; `generic` installs to `.agents/skills`; `claude-code` installs to `.claude/skills`; `kimi-code` installs to `.kimi-code/skills`.

Install the DeepSci extension when a project needs the research pipeline skills:

```bash
isomer-cli system-skills install --target codex --extension deepsci
```

Inspect or remove Isomer-owned projections with:

```bash
isomer-cli system-skills status --target codex
isomer-cli system-skills uninstall --target codex
```

## Getting Started With CLI Agent

After the CLI and skills are installed, drive Isomer from your coding agent with short skill calls and follow-up prompts.

### Create the Research Topic

The user starts with a concrete research goal and wants the agent to turn it into an Isomer Research Topic with durable intent files.

User Action:

> $isomer-op-topic-creator create topic: Investigate the concrete research question and define the expected evidence.

AI:

> Created the Research Topic, wrote the topic overview and environment gate, and stopped for review.

### Prepare the Topic Workspace

The user wants the agent to set up only what the topic needs, verify the environment, and report blockers before research begins.

User Action:

> $isomer-op-topic-creator run-to setup-topic-env

AI:

> Prepared the Topic Workspace, verified dependencies, and reported readiness or blockers.

### Run a Bounded Research Pass

The user wants one controlled research pass, not unattended automation, and expects the agent to return artifacts plus a next route.

User Action:

> $isomer-deepsci-pipeline empirical-pass

AI:

> Ran a bounded research pass, recorded artifacts, and reported the next route.

### Tighten the Evidence

The user sees that a claim needs stronger evidence and asks the agent to separate what is already supported from what must be measured next.

User Prompt:

> Tighten the evidence: compare the model against real measurements, explain mismatches, and revise the next experiment.

AI:

> Separated supported claims from missing evidence and proposed a follow-up pass.

### Write the Paper

The user wants the accepted records turned into a readable paper artifact, with review blockers surfaced rather than hidden.

User Action:

> $isomer-deepsci-pipeline paper-pass

AI:

> Drafted or revised the paper from accepted records, built the artifact, and reported review blockers.

For concrete prompt and response patterns, start with [Research Workflow Tutorials](docs/tutorial/index.md).

## Documentation

- [Documentation Home](docs/index.md)
- [Quickstart](docs/tutorial/quickstart.md)
- [Research Workflow Tutorials](docs/tutorial/index.md)
- [CLI Reference](docs/manual/cli-reference.md)
- [Concepts](docs/manual/concepts.md)
- [Developer Guide](docs/developer/index.md)

## Status

The project is early but usable for local research-project setup, topic workspace management, record indexing, and GUI inspection. See [Assumptions and Roadmap](docs/developer/assumptions-and-roadmap.md) for current boundaries.

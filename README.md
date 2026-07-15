# isomer-labs

Documentation: https://codegandee.github.io/isomer-labs/

Isomer Labs is a research workbench for running multi-agent research topics from a project directory. It gives operators a CLI, packaged system skills, topic workspaces, durable records, and a local web GUI for inspecting how ideas, experiments, and artifacts evolve.

**Note:** Isomer Labs is designed to be driven by a CLI agent. The recommended usage pattern is to install the Isomer system skills, then ask your CLI agent to operate Isomer through those skills and `isomer-cli`.

## Prerequisites

Isomer Labs depends on [Pixi](https://github.com/prefix-dev/pixi) for project and Topic Workspace environments. The recommended Pixi install method on Linux and macOS is:

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

Paper-writing workflows need a TeX renderer. [Tectonic](https://github.com/tectonic-typesetting/tectonic) is recommended; a standard LaTeX distribution also works when a project already depends on it. Install Tectonic as a Pixi global tool with:

```bash
pixi global install tectonic
```

[Houmao](https://github.com/igamenovoer/houmao) is optional. Install it when you want Houmao-backed agent-team construction, Topic Service Master setup, managed agents, gateways, mailboxes, and related adapter features:

```bash
uv tool install houmao
```

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

Install packaged Isomer skills with `isomer-cli system-skills install`. The core group includes the entrypoint and `isomer-op-system-skill-mgr`; together they route known tasks and reconcile optional extensions from the current operator host.

Discover optional agent-skill extensions and inspect their entry skills, public commands, and installation guidance before selecting one:

```bash
isomer-cli system-skills extensions list
isomer-cli system-skills extensions show kaoju
```

```bash
isomer-cli system-skills install --target codex --scope user
```

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`. Every target-resolving command requires `--scope user|project`. Project scope uses the exact current working directory; user scope installs for the current OS user.

| Target | Project Scope | User Scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

Use project scope for skills confined to the current working directory. Choose user scope intentionally when the skills should be available to the selected host across Projects.

Install the DeepSci extension when a project needs the research pipeline skills:

```bash
isomer-cli system-skills install --target codex --scope user --extension deepsci
```

Install Kaoju when a project needs evidence-led literature and codebase surveys, first-hand method trials, or controlled comparisons. After installation, enter the extension through `$isomer-kaoju-pipeline` rather than `isomer-cli ext kaoju`.

```bash
isomer-cli system-skills install --target codex --scope user --extension kaoju
```

Inspect or remove Isomer-owned projections with:

```bash
isomer-cli system-skills status --target codex --scope user
isomer-cli system-skills uninstall --target codex --scope user
```

Direct CLI detection is read-only and inspects only roots supplied by the caller. With no root, it reports declarations and catalog state without scanning provider directories:

```bash
isomer-cli --print-json project system-extensions detect
isomer-cli --print-json project system-extensions detect --skill-root /explicit/agent/skill-root
isomer-cli project system-extensions remember kaoju
```

For normal agent-driven operation, use `$isomer-op-system-skill-mgr`. It trusts existing Project declarations, checks Isomer receipts in roots known to the current host, falls back to the host-visible skill inventory, and adds complete extensions to the Project during authorized reconciliation or installation unless the user opts out. It never removes a declaration because a different agent lacks the same installation. A new installation may require a new turn, thread, or host-native skill reload.

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

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

- `intent/` stores the topic overview, environment gate, actor definitions, derived setup gates, and non-canonical user-editable Kaoju template working copies under `intent/derived/writing-template/<name>/`.
- `records/` stores durable research records, artifacts, evidence items, decisions, view manifests, and the SQLite index used by the GUI.
- `runtime/` stores Workspace Runtime state, adapter payloads, launch material, and resumable execution state.
- `repos/topic-main/` is the topic-owned development repository for code-bearing work.
- `repos/extern/` stores canonical external repositories such as upstream source checkouts.
- `actors/` and `agents/` store actor or agent workspaces, usually as worktrees of `repos/topic-main`.

The Project Manifest records where each Topic Workspace lives, while `topic-workspace.toml` inside the workspace binds semantic labels such as `topic.repos.main`, `topic.records`, and `topic.runtime` to concrete paths. Agents and skills should resolve those labels instead of guessing paths.

## Install System Skills

Install packaged Isomer skills with `isomer-cli system-skills install`. The core installation unit is the public `isomer-op-entrypoint` pack. Operator, service, shared-support, and research-recording capabilities, including system-skill management, remain protected members routed by that parent.

Discover optional agent-skill extensions and inspect their entry skills, public commands, and installation guidance before selecting one:

```bash
isomer-cli system-skills extensions list
isomer-cli system-skills extensions show kaoju
```

```bash
isomer-cli system-skills install --target codex
isomer-cli system-skills install --target codex --scope user
```

Supported targets are `claude-code`, `codex`, `kimi-code`, `generic`, and `all`. When `--scope` is omitted, `system-skills install` defaults to Project scope at the exact current working directory and does not search ancestor Git or Isomer roots. Explicit `--scope project` is equivalent, while `--scope user` is the only route to user-wide installation. `system-skills status`, `upgrade`, and `uninstall` require an explicit `--scope user|project`.

| Target | Project Scope | User Scope |
| --- | --- | --- |
| `claude-code` | `<cwd>/.claude/skills` | `${CLAUDE_CONFIG_DIR:-~/.claude}/skills` |
| `codex` | `<cwd>/.agents/skills` | `${CODEX_HOME:-~/.codex}/skills` |
| `kimi-code` | `<cwd>/.kimi-code/skills` | `${KIMI_CODE_HOME:-~/.kimi-code}/skills` |
| `generic` | `<cwd>/.agents/skills` | `~/.agents/skills` |

Use project scope for skills confined to the current working directory. Choose user scope intentionally when the skills should be available to the selected host across Projects.

Install the DeepSci extension when a project needs hypothesis-driven production research. The selector installs core plus the complete `isomer-ext-deepsci-entrypoint` pack:

```bash
isomer-cli system-skills install --target codex --extension deepsci
```

Install Kaoju when a project needs evidence-led literature and codebase surveys, first-hand method trials, or controlled comparisons. The selector installs core plus the complete `isomer-ext-kaoju-entrypoint` pack:

```bash
isomer-cli system-skills install --target codex --extension kaoju
```

The Kaoju pack contains 16 protected members, including `paper-search`. Paper-search performs bounded provider retrieval through agent-available external tools and records one provider-neutral observation per logical action. Discovery keeps search strategy, candidate selection, and Reading List ownership. `isomer-cli ext research literature` provides local-only observation recording, derived queries, and explicit index rebuild or validation; it never proxies a literature provider.

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

For newcomer orientation, invoke `$isomer-op-welcome`; for normal agent-driven operation, use `$isomer-op-entrypoint use system-skills to <task>`. The protected manager reads Project declarations, current v5 receipts, explicit-root integrity, and limited live inventory in that order. It registers only verified current-v5 complete packs and never removes a declaration because another agent lacks the same installation. Refresh the host or start a new session after installation or upgrade.

## Getting Started With CLI Agent

After the CLI and skills are installed, drive Isomer from your coding agent with short skill calls and follow-up prompts.

### Create the Research Topic

The user starts with a concrete research goal and wants the agent to turn it into an Isomer Research Topic with durable intent files.

User Action:

> $isomer-op-entrypoint use topic-create to create a topic that investigates the concrete research question and defines the expected evidence

AI:

> Created the Research Topic, wrote the topic overview and environment gate, and stopped for review.

### Prepare the Topic Workspace

The user wants the agent to set up only what the topic needs, verify the environment, and report blockers before research begins.

User Action:

> $isomer-op-entrypoint use topic-create to run through setup-topic-env

AI:

> Prepared the Topic Workspace, verified dependencies, and reported readiness or blockers.

### Run a Bounded Research Pass

The user wants one controlled research pass, not unattended automation, and expects the agent to return artifacts plus a next route.

User Action:

> $isomer-ext-deepsci-entrypoint use empirical-pass to run one bounded research pass

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

> $isomer-ext-deepsci-entrypoint use paper-pass to draft the paper from accepted records

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

## Related Projects

- [academic-research-skills](https://github.com/imbad0202/academic-research-skills) — a collection of prompts and skills for academic research workflows.
- [paper-qa](https://github.com/Future-House/paper-qa) — a framework for scientific literature question answering and review synthesis.
- [deer-flow](https://github.com/bytedance/deer-flow/tree/main) — a deep research flow framework for autonomous scientific discovery.
- [agent-paper-grounded-reading](https://github.com/c-narcissus/agent-paper-grounded-reading) — an agentic paper reading workflow grounded in source evidence.
- [adhd-paper-reader](https://github.com/iagomsouza/adhd-paper-reader) — a focused, distraction-free paper reader and summarizer.
- [paper-with-code-skills](https://github.com/Gojay001/paper-with-code-skills) — skills and workflows for reading and reproducing papers with code.

## Acknowledgments

The DeepSci skill family originated from the [DeepScientist project](https://github.com/ResearAI/DeepScientist). Isomer Labs completely refactored those skills to fit its system-skill architecture, Project and Topic Workspace model, artifact contracts, and operating workflows. We thank the DeepScientist authors for their work and inspiration.

## Status

The project is early but usable for local research-project setup, topic workspace management, record indexing, and GUI inspection. See [Assumptions and Roadmap](docs/developer/assumptions-and-roadmap.md) for current boundaries.

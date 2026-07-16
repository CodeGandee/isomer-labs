# Tutorial Overview

Tutorials are short, sequential guides for operators. Start with project creation, then follow the research workflow pages when you are ready to conduct a topic.

The research workflow pages use the local `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` workspace as a concrete case. Each page explains the task, the prompt pattern, and the skill call pattern because Isomer's main user experience is driving agents through system skills such as `$isomer-op-topic-creator`, `$isomer-op-topic-mgr`, and `$isomer-deepsci-pipeline`.

When a requested research target lacks a producible prerequisite, the system skills pause before prerequisite mutation and offer a target-scoped run-to choice alongside next-prerequisite-only, alternate-route, and stop choices. Run-to is explicit prompt-level authorization, not an `isomer-cli` command, global yes-to-all flag, Project setting, or Run-level Control Mode. It preserves separate owner Runs and human Gates and stops after the named target.

## Project Creation

- [Quickstart](quickstart.md) installs the released CLI, initializes a Project, and validates it.
- [Create a Project](first-project.md) explains the project directory setup.

## Research Workflow

- [Author Research Intent](author-research-intent.md)
- [Prepare Topic Environment](prepare-topic-environment.md)
- [Run a Human-Steered Research Pass](run-a-human-steered-research-pass.md)
- [Validate With Real Evidence](validate-with-real-evidence.md)
- [Develop a White-Box Model](develop-a-white-box-model.md)
- [Write and Inspect a Paper](write-and-inspect-a-paper.md)

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)

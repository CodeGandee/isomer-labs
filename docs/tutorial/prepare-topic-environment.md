# Prepare Topic Environment

This tutorial shows how to prompt an Isomer-equipped agent to prepare a Topic Workspace after the research intent is clear. The task is to turn the environment gate into a verified workspace, not to manually remember every setup command.

## Starting Point

You have a Research Topic with `intent/src/topic-overview.md` and `intent/src/topic-env-gate.md`. In the running example, the topic needs Python modeling libraries, B200 host facts, `ncu`, and source repositories such as FlashAttention and AccelSim.

## Task

Ask the agent to read the topic environment gate, derive the setup plan, install or verify required dependencies, capture host facts, acquire required repositories, and report readiness with blockers. Use the topic-creator or topic environment setup skill as the entrypoint; treat setup as incomplete until the agent can name what passed and what remains blocked.

## Example Interaction

User Action:

> $isomer-op-topic-creator run-to setup-topic-env

AI:

> Routed from topic creation into topic environment setup.
>
> Read the topic environment gate before mutating the workspace.

User Prompt:

> Now setup topic env.

AI:

> Topic environment setup is complete and verified.
>
> Created the Pixi environment, topic-main guidance files, and derived environment gate.
>
> Verified Python 3.11, NumPy, SymPy, SciPy, Markdown, and `ncu`.
>
> Blockers: none.

User Prompt:

> Verify if you can use `ncu`.

AI:

> `ncu` is available on the B200 host.
>
> Reported the `ncu` version and path.
>
> Ran a tiny profiling smoke test and captured SM, L1, L2, DRAM, and occupancy counters.

User Prompt:

> Use the official FlashAttention repository as the algorithm source. Acquire only the source we need, and default to a shallow clone unless the topic requires history.

AI:

> Resolved the repository binding for `topic.repos.flash-attention`.
>
> Acquired or reused the repository at `repos/extern/flash-attention`.
>
> Recorded why a snapshot is sufficient, or why full history is required.

## How to Steer

Ask the agent to show readiness evidence, not optimism. If it says a dependency is ready, ask what command proved it. If a repository appears in the filesystem but not the topic manifest, ask the agent to register or resolve the semantic path instead of relying on the directory name.

Useful steering prompts:

User Action:

> $isomer-srv-topic-env-setup verify-env-gate

User Prompt:

> Read the topic env gate and summarize the runnable target before installing anything.

User Prompt:

> Capture B200 host facts: GPU model, driver, CUDA version, memory, clocks, and `ncu` path.

User Prompt:

> Show the readiness report. Separate verified items, skipped items, and blockers.

## Under the Hood

The agent usually routes through `isomer-op-topic-creator` and `isomer-srv-topic-env-setup`. For debugging, the low-level checks look like this:

```bash
isomer-cli --print-json project validate --topic flash-attention-4-whitebox-runtime-model
isomer-cli --print-json project paths list --topic flash-attention-4-whitebox-runtime-model
isomer-cli --print-json project runtime inspect --topic flash-attention-4-whitebox-runtime-model
isomer-cli --print-json project runtime validate --topic flash-attention-4-whitebox-runtime-model --require-ready-readiness
```

The local example records the derived setup plan in `intent/derived/isomer-env-gate.md` and the final readiness summary in `isomer-topic-workspace-summary.md`.

## What Good Looks Like

The Topic Workspace has a verified Pixi environment, recorded host facts, resolved repository bindings, and a readiness summary. The agent can explain which checks passed and which research actions are now safe.

## Common Pitfalls

Do not let the agent silently skip required tools. Do not confuse a cloned source tree with a registered topic repository. Do not let failed setup disappear into later research claims.

## Next Tutorial

Continue to [Run a Human-Steered Research Pass](run-a-human-steered-research-pass.md).

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)

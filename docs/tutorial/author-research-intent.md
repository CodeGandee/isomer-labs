# Author Research Intent

This tutorial shows how to drive an Isomer-equipped agent from a broad research idea to a concrete Research Topic. The task is not to fill a form; it is to keep prompting until the agent has written a topic overview, a topic environment gate, and a clear stop point before setup.

## Starting Point

You have an Isomer Project, installed system skills, and an operator agent that can use them. The running example is the local `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` workspace.

## Task

Ask the agent to create the topic, then refine the intent until it names the target system, evidence standard, expected outcome, required tools, and setup boundary. In normal use, start by invoking an operator skill or by asking the agent to route to one; the agent should stop at `define-topic-env` when the topic is clear enough for you to review before environment setup.

## Example Interaction

User Action:

> $isomer-op-entrypoint use help to show the available research paths

AI:

> Showed the operator menu.
>
> Recommended `isomer-op-topic-creator` for starting manual research with a human-orchestrated Topic Actor.

User Prompt:

> Create a topic. We want to develop a white-box math model of FlashAttention 4 runtime, so we can predict runtime in ms from the input. The model must follow the GPU execution model, not fit a black-box function to measurements.

AI:

> Created the Research Topic and stopped at `define-topic-env`.
>
> Wrote `intent/src/topic-overview.md` and `intent/src/topic-env-gate.md`.
>
> The next action is to review the environment gate before setup.

User Prompt:

> We are targeting B200 GPUs, and we have them on this host.

AI:

> Updated the topic intent for NVIDIA B200.
>
> Verified the host has B200 GPUs and `ncu` is available.
>
> The environment gate is now concrete enough to proceed to `setup-topic-env`.

User Prompt:

> The white-box model must include B200 system architecture, execution flow, internal hardware specifics, closed-form formulas, and probabilistic models for random effects like cache misses. Before editing, search online for GPU runtime modeling methods.

AI:

> Searched current GPU runtime-modeling references.
>
> Updated the intent to require B200 execution-flow decomposition, stage formulas, probabilistic cache and memory models, and NCU validation.
>
> Added relevant source links to the topic overview.

## How to Steer

If the topic is vague, name the missing dimension directly: target hardware, forward or backward pass, supported precisions, validation evidence, or expected artifact. If the agent starts setup too early, tell it to stop at the topic environment gate and summarize what still needs your review.

Useful steering prompts:

User Action:

> $isomer-op-entrypoint use topic-create to clarify the research intent

User Prompt:

> Clarify the topic before setup. Lock the target hardware, algorithm source, validation standard, expected output, and out-of-scope work.

User Prompt:

> Do not proceed to setup yet. Show me the topic overview and environment gate summary first.

User Prompt:

> Add NCU validation, but make clear that NCU is validation evidence, not an input required for every prediction.

## Under the Hood

The agent usually routes through `isomer-op-topic-creator`. It may use low-level commands like these to register the topic and resolve the intent file:

```bash
isomer-cli project topics create flash-attention-4-whitebox-runtime-model \
  --statement "Develop a white-box model that predicts FlashAttention 4 forward runtime on NVIDIA B200." \
  --set-default
isomer-cli --print-json project paths get topic.intent.overview --topic flash-attention-4-whitebox-runtime-model
```

You normally do not need to run those commands yourself. Use prompts to drive the agent unless you are debugging a failed topic registration.

## What Good Looks Like

The topic overview states the exact research question, scope, exclusions, evidence standard, and expected outcome. The environment gate says what must be installed, cloned, measured, or verified before research begins.

For the FlashAttention case, a good intent names forward pass only, NVIDIA B200, official FlashAttention source, BF16/FP16/FP8/FP4 support, a runnable Python predictor, a documented derivation, runtime comparison, and NCU counter evidence.

## Common Pitfalls

Do not accept a topic just because the directory exists. Do not let proxy evidence become the final validation standard. Do not postpone exclusions such as backward pass, multi-GPU execution, or unsupported precisions.

## Next Tutorial

Continue to [Prepare Topic Environment](prepare-topic-environment.md).

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)

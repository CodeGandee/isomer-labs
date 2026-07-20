# Develop a White-Box Model

This tutorial shows how to prompt the agent to improve a model as an inspectable execution-flow artifact. The task is to make the model explain runtime, saturated hardware, and blocking path, not merely fit output numbers.

## Starting Point

You have an initial model and some evidence. In the running example, the user repeatedly pushed the agent from a runtime predictor toward B200 execution-flow models: per-SM reservations, sub-core partitions, and SASS-level critical paths.

## Task

Ask the agent to compare candidate models against the topic goal, choose the most relevant model, and revise the model when evidence reveals a mismatch. Use explicit DeepSci skill calls when you want a bounded modeling pass, a hypothesis pass, or a paper update pass.

## Example Interaction

User Action:

> $isomer-ext-deepsci-entrypoint use hypothesis-pass to deepen the hardware model by inspecting AccelSim's NVIDIA GPU simulation implementation, deriving ideas, selecting a minimal workflow, and proceeding

AI:

> Routed through a minimal research pass.
>
> Studied simulator references and produced modeling ideas for inner-GPU components.

User Prompt:

> Follow the selected pass in `isomer-ext-deepsci-entrypoint` and propose more detailed execution-flow analytical models. Do idea -> experiment -> paper update for three rounds.

AI:

> Completed three refinement rounds.
>
> Round 1: per-SM execution-unit reservation model.
>
> Round 2: sub-core partition scheduling model.
>
> Round 3: SASS-level RAW critical-path model.
>
> Updated the paper and saved evidence artifacts.

User Prompt:

> Now we have three models. Which one is best?

AI:

> Compared the models by the topic goal.
>
> Identified the model that best predicts saturated component and blocking path.
>
> Recommended keeping runtime-focused variants as alternatives rather than the main contribution.

User Prompt:

> For reviewer evidence, design experiments that saturate each part of the critical path and show prediction matches NCU evidence.

AI:

> Proposed a per-node saturation matrix.
>
> Mapped each target path segment to input shapes and NCU metrics.
>
> Defined success criteria for component-level accuracy, path-level accuracy, and runtime error.

## How to Steer

When the model drifts toward generic runtime prediction, restate the topic goal: predicted runtime, predicted saturated component, and predicted blocking path. Ask the agent to move alternatives into an appendix or supporting record when they are useful but not central.

Useful steering prompts:

User Action:

> $isomer-ext-deepsci-entrypoint use empirical-pass to test critical-path saturation, collect hard evidence, and present it in the paper

User Prompt:

> Compare the candidate models against the stated topic goal. Which one should be the proposed method, and which ones are alternatives?

User Prompt:

> Explain how input shape flows through hardware stages before producing the final prediction.

User Prompt:

> For every random effect, name the probability model or the evidence gap instead of hiding it in a fitted constant.

## Under the Hood

The local example stores model code under `repos/topic-main/src/fa4_b200_predictor/` and research records under `records/artifacts/research-records/`. DeepSci skills should preserve model choices, rejected alternatives, revisions, and evidence as records with lineage rather than relying on ad hoc Markdown notes.

## What Good Looks Like

The model has an inspectable path from input to prediction. A reader can identify each stage, hardware component, formula or probabilistic term, and aggregation rule.

## Common Pitfalls

Do not choose the most accurate model if it no longer answers the research question. Do not let code variable names become the paper notation. Do not collapse data movement, scheduling, and instruction issue into one unexplained constant.

## Next Tutorial

Continue to [Write and Inspect a Paper](write-and-inspect-a-paper.md).

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)

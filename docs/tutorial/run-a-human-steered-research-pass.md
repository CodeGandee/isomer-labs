# Run a Human-Steered Research Pass

This tutorial shows how to run research as a controlled conversation with an Isomer-equipped agent. The task is to choose a bounded pass, inspect what the agent produced, then continue, redirect, pause, or demand stronger evidence.

## Starting Point

You have a prepared Topic Workspace and a next research objective. In the running example, the user repeatedly asked for empirical passes, hypothesis passes, analysis passes, and paper updates, then corrected the agent when evidence or presentation was weak.

## Task

Prompt the agent with the research move you want, or explicitly invoke the DeepSci pipeline skill when you know the route. The agent should route to the appropriate DeepSci skill or pipeline, report stage status, produce durable records or artifacts, and tell you what next decision is needed.

## Example Interaction

User Action:

> $isomer-deepsci-pipeline list passes

AI:

> Listed available passes: `empirical-pass`, `hypothesis-pass`, `paper-pass`, `revision-pass`, `polish-pass`, and `submission-pass`.
>
> No pass was executed.

User Prompt:

> Do an empirical pass using the topic workspace operator workspace.

AI:

> Started an empirical pass.
>
> Completed scout, baseline, and idea stages.
>
> Experiment is running in the background.
>
> Next: interpret the experiment result and produce a pipeline terminal report.

User Prompt:

> What test has been done?

AI:

> Separated project unit tests from research-model tests.
>
> Reported predictor metrics on validation configurations.
>
> Stated clearly that the current model had not yet been tested against real B200 silicon.

User Prompt:

> Continue to do experiment.

AI:

> Started a bottleneck-refinement hypothesis pass.
>
> Named the hypothesis, target metrics, and expensive run stage.
>
> Reported when the pass completed, which records were created, and what next analysis route was recommended.

## How to Steer

Research passes work best when you keep the next move narrow. Ask for one modeling pass, one experiment, one analysis, or one paper revision. After the agent responds, inspect the artifacts and decide whether the next prompt should continue the same line or change direction.

Useful steering prompts:

User Action:

> $isomer-deepsci-pipeline hypothesis-pass

User Prompt:

> Summarize the generated records and artifacts. Which claim do they support, and what evidence is still missing?

User Prompt:

> Pause before the expensive run stage and ask for approval.

User Prompt:

> This result points to a modeling gap. Route to analysis and propose the next experiment.

## Under the Hood

The agent may use `isomer-op-entrypoint`, `isomer-deepsci-pipeline`, or individual DeepSci skills such as `isomer-deepsci-scout`, `isomer-deepsci-idea`, `isomer-deepsci-experiment`, and `isomer-deepsci-analysis`. Those skills use `isomer-cli` internally to resolve latest context, write records, attach lineage, and render readable views.

## What Good Looks Like

A good pass ends with a concrete artifact, record id, evidence class, blocker, or next route. It should not end with only "I worked on it" or "the model improved."

## Common Pitfalls

Do not let one prompt turn into an uncontrolled research spree. Do not accept progress without artifact locations. Do not treat a failed pass as wasted work; the failure often identifies the next best prompt.

## Next Tutorial

Continue to [Validate With Real Evidence](validate-with-real-evidence.md).

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)

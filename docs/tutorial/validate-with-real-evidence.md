# Validate With Real Evidence

This tutorial shows how to prompt the agent when a research claim needs stronger evidence. The task is to prevent proxy evidence, emulator evidence, or noisy measurements from being reported as real-hardware proof.

## Starting Point

You have a candidate model, hypothesis, or result. In the running example, the agent first reported good model error against an emulator; the user pushed back and forced the distinction between theoretical-model checks and actual B200 runs.

## Task

Ask the agent what evidence was actually used, whether it matches the claim, and what experiment would turn the claim into real evidence. When the evidence requirement changes, explicitly invoke the topic manager or DeepSci pipeline skill so the requirement becomes part of the durable topic workflow.

## Example Interaction

User Prompt:

> No, I mean test data into the theoretical model vs actual run.

AI:

> No actual B200 kernel runs have been done yet.
>
> The reported error is against a high-fidelity emulator, not real silicon.
>
> To know real error, run the FA4 kernel on B200 and compare measured runtime with predicted runtime.

User Prompt:

> Without actually running something on B200, how do you know the error?

AI:

> We do not know the real error.
>
> The reported MAPE means the predictor matches the emulator, not the real GPU.
>
> The honest conclusion is conditional until real B200 measurements are collected.

User Action:

> $isomer-op-topic-mgr tighten the topic requirement, we must have theoretical vs actual run data

AI:

> Tightened the topic requirement.
>
> Recorded that real theoretical-versus-actual run data is required before claiming model accuracy.

User Prompt:

> To make the model stronger, prove that it can predict bottlenecks by pushing inputs to saturate compute, storage, memory, or bandwidth. Do a hypothesis pass.

AI:

> Created a saturation hypothesis and experiment contract.
>
> Paused before the expensive NCU profiling stage for approval.
>
> Planned configs to target MMA, MUFU, HBM, L2, SMEM, and TMA regimes.

User Prompt:

> Note that the GPU is very busy right now; your previous testing may be inaccurate.

AI:

> Checked `nvidia-smi` and found high GPU utilization.
>
> Marked the NCU results as suspect.
>
> Recorded amended results and recommended rerunning on an idle GPU before adopting the model change.

## How to Steer

Ask the agent to name the evidence class before accepting the claim. If the agent reports a number, ask whether it came from emulator, simulator, synthetic data, microbenchmark, NCU, or real hardware. If the GPU is noisy or busy, ask it to downgrade confidence and record that caveat.

Useful steering prompts:

User Action:

> $isomer-deepsci-pipeline design experiment to prove these, collect hard evidence, and present them in appendix and main text

User Prompt:

> Separate proxy evidence from real-hardware evidence. What claim is actually supported?

User Prompt:

> Design an NCU experiment that compares predicted saturated component, predicted blocking path, and predicted runtime against measured evidence.

User Prompt:

> If the experiment disagrees with the model, analyze why and propose a model revision instead of hiding the mismatch.

## Under the Hood

DeepSci experiment and analysis skills write structured evidence records and route decisions. The CLI record and lineage APIs keep measurements, findings, and follow-up decisions connected so later GUI views can show why a claim was accepted, downgraded, or revised.

## What Good Looks Like

The validation report separates predicted runtime, measured runtime, predicted saturated component, measured counter evidence, mismatch analysis, and confidence. It says which evidence class supports each claim.

## Common Pitfalls

Do not let emulator accuracy become real-hardware accuracy by wording drift. Do not accept vague bottleneck labels like "compute-bound" when the topic asks for saturated component and blocking path. Do not hide failed or noisy runs.

## Next Tutorial

Continue to [Develop a White-Box Model](develop-a-white-box-model.md).

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)

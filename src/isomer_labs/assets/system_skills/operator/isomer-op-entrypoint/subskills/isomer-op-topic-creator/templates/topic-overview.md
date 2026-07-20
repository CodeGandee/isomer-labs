# Research Topic: `<topic-title>`

Write one clear research question or investigation intent. Keep it concrete, scoped, and grounded in the evidence or method the research should use.

> How can we predict Flash Attention 4 runtime on the GPU available on the host, while keeping the prediction explainable and tied to the actual kernel and hardware?

## Motivation

State why this topic matters and what uncertainty makes it worth investigating. Use short bullets and focus on intent, not detailed methodology.

> - Estimate runtime without measuring every possible input.
> - Explain why one input or kernel variant is faster than another.
> - Keep measurements as support for calibration and validation, not the main answer.

## Topic Breakdown

Use this section to set the topic's working boundaries. Keep each point direct enough that another agent can follow it without guessing.

> Use the host GPU as the target, keep the model explainable, and avoid turning the work into a black-box timing fit.

### Do's

List the actions, evidence, outputs, and constraints the research should honor. Prefer concise bullets that start with concrete verbs.

> - Discover the host GPU before making GPU-specific claims.
> - Predict runtime as `predicted_runtime_ms` for `{host_gpu_model}`.
> - Prefer a white-box explanation over a fitted timing curve.

### Don'ts

List the non-goals and forbidden shortcuts. Phrase each point as a clear boundary, not as a long explanation.

> - Do not hard-code a GPU before `{host_gpu_model}` is materialized.
> - Do not make measured timings the primary prediction method.
> - Do not require timeline or budget sections.

## Expected Outcome

Name the concrete outputs the research should leave behind. Keep the list short and include caveats or follow-up inquiries when the answer may be incomplete.

> - Host GPU discovery evidence.
> - Prediction records with `predicted_runtime_ms`.
> - Short explanations for predicted runtimes.
> - Caveats when evidence or model scope is limited.

## Related Links

List only links that should anchor the work. Use a short label and the raw URL.

> - Flash Attention GitHub repository: https://github.com/Dao-AILab/flash-attention

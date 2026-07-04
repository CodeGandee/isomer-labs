# Research Topic: Flash Attention 4 Runtime Prediction on `{host_gpu_model}`

How can we predict Flash Attention 4 runtime on the GPU available on the host, while keeping the prediction explainable and tied to the actual kernel and hardware?

## Motivation

- Avoid assuming a fixed GPU before the topic is materialized.
- Estimate runtime without measuring every possible input.
- Explain why one input or kernel variant is faster than another.
- Keep measurements as support for calibration and validation, not the main answer.

## Topic Breakdown

### Do's

- Discover the host GPU before making GPU-specific claims.
- Predict runtime as `predicted_runtime_ms` for `{host_gpu_model}`.
- Use Flash Attention 4 inputs, kernel artifacts, and host GPU facts as model evidence.
- Prefer a white-box explanation over a fitted timing curve.
- Show the main reason behind each prediction.
- Keep validation inputs separate from prediction-query inputs.

### Don'ts

- Do not hard-code a GPU before `{host_gpu_model}` is materialized.
- Do not make measured timings the primary prediction method.
- Do not use a neural model or regressor as the main model.
- Do not require timeline or budget sections.

## Expected Outcome

- Host GPU discovery evidence.
- A runtime prediction model for `{host_gpu_model}`.
- Prediction records with `predicted_runtime_ms`.
- Short explanations for predicted runtimes.
- Caveats when evidence or model scope is limited.

## Related Links

- Flash Attention GitHub repository: https://github.com/Dao-AILab/flash-attention

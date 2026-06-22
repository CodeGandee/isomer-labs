# Research Topic: Flash Attention 4 Runtime Prediction on DGX Spark GB10

How can we predict the Flash Attention 4 runtime on DGX Spark GB10 by building a theoretical performance model that matches the kernel execution, using the kernel design, computation process, memory access pattern, and GPU execution model to estimate how much time each part consumes and how to aggregate those parts, while allowing measured runtimes only to tune internal model parameters rather than serve as the primary fitting target?

## Motivation

- Derive rough runtime estimates directly from the kernel input and code artifacts without needing to execute the kernel on real GPU hardware for every query.
- Produce interpretable results that identify which kernel stage, memory pattern, or GPU subsystem is the bottleneck for a given input.
- Attribute acceleration or slowdown across variants of the same kernel, so that changes in kernel design can be predicted to speed up or slow down the runtime before implementation.

## Topic Breakdown

### Do's

- Predict Flash Attention 4 runtime as a scalar value in milliseconds on the DGX Spark GB10 GPU.
- Build a theoretical performance model that reflects the actual kernel execution.
- Base the model on kernel design, computation process, and memory access pattern.
- Use the GPU execution model, including GB10 architecture specifics, to estimate time consumed by each execution part.
- Aggregate per-part time estimates according to how the GPU executes the kernel.
- Use measured runtimes only for tuning internal model parameters or validating model behavior.
- Maintain traceability from the Flash Attention 4 input description through CUDA kernel source code, PTX, and SASS to the predicted runtime and component-time explanation.

### Don'ts

- Treat the problem as a black-box curve-fitting task, such as proposing a parameterized math formula whose parameters are fit primarily to measured timings.
- Train a neural network or other regressor to fit measured runtimes without a matching theoretical execution model.

## Related Links

- Flash Attention GitHub repository: https://github.com/Dao-AILab/flash-attention

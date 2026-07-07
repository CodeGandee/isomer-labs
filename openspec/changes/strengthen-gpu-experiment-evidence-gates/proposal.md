## Why

The GPU analytical-modeling user plugin already separates evidence classes and model-shape claims, but its experimentation guidance should be sharper about the generic evidence gates that make a hardware-grounded analytical model credible. The missing contract is not topic-specific infrastructure; it is that bottleneck predictions need matching hard observations, latency models need predicted-versus-measured latency, and final reports need to show the hard evidence.

## What Changes

- Strengthen `gpu-evidence-and-experiment` so bottleneck-oriented experiments must intentionally stress one predicted component or blocking path at a time and collect hard evidence that supports or refutes the prediction.
- Strengthen evaluation guidance so any proposed analytical latency model must compare predicted latency against measured latency before making latency-accuracy claims.
- Strengthen reporting and closure guidance so final papers or reports must show hard evidence for central runtime, saturated-component, and blocking-path claims rather than only summarizing conclusions.
- Keep the strengthened guidance generic to GPU kernel analytical modeling and avoid hard-coding a specific kernel, GPU SKU, topic workspace, host setup, command wrapper, paper venue, or artifact path.
- Keep the change project-local under `skillset/user-plugins/gpu-analytical-modeling`; do not modify packaged system skills, callback registry behavior, CLI behavior, or distribution assets.

## Capabilities

### New Capabilities

- `gpu-experiment-evidence-gates`: Project-local user-plugin guidance for generic GPU analytical-modeling experiment gates: one-component bottleneck proof, predicted-versus-measured latency validation, and final hard-evidence reporting.

### Modified Capabilities

- None.

## Impact

- Affected files are expected to stay under `skillset/user-plugins/gpu-analytical-modeling/` and this change directory.
- No Python APIs, CLI commands, packaged system skills, distribution manifests, or callback registry behavior should change.
- Validation should use skill-file inspection, local metadata checks, and the available skill validator for touched skill directories.

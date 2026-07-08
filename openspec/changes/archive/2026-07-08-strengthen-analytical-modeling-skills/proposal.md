## Why

The GPU analytical-modeling user plugin already guards against broad evidence and claim mistakes, but prior topic chatlog analysis shows a sharper analytical-modeling gap: agents still need stronger instruction about what it means to develop an analytical model built on hardware modeling rather than a coarse bandwidth formula, black-box fit, or simulator-shaped narrative.

This change strengthens the project-local plugin so callback agents require interpretable, hardware-grounded models: parameters with physical meaning, explicit internal hardware components, execution paths, bottleneck formation rules, and verification that predicted bottlenecks match observed bottleneck evidence.

## What Changes

- Strengthen `gpu-modeling-method` so an analytical model is defined as an interpretable mapping from workload inputs to hardware-component behavior, execution path timing, bottleneck selection, and predicted runtime.
- Add or revise command guidance so agents require model parameters to have physical meanings, units, sources, bounds, and named interpretation instead of acting as anonymous fit coefficients.
- Add or revise command guidance so agents model internal hardware components, data movement, scheduling/issue limits, overlap, serialization, and pipeline aggregation when those mechanisms explain runtime or bottlenecks.
- Make closed-form or bounded analytical expressions the preferred representation, with stochastic behavior represented by named probabilistic terms, expected values, bounds, or validity limits.
- Require verification framing that compares predicted bottleneck component/path against observed bottleneck evidence, not only runtime error.
- Clarify that simulator projects such as AccelSim/GPGPU-Sim are architecture/modeling references, not executable truth sources for target hardware unless separately validated.
- Require all strengthened instructions to remain generic to GPU kernel analytical modeling, without tying the plugin to a specific kernel, GPU SKU, topic workspace, paper, host, or environment setup.
- Keep the change project-local under `skillset/user-plugins/gpu-analytical-modeling`; do not modify packaged system skills, callback registry behavior, CLI behavior, or distribution assets.

## Capabilities

### New Capabilities

- `gpu-analytical-modeling-skill-guidance`: Project-local user-plugin skill guidance for GPU kernel analytical modeling, including execution-flow model shape, evidence boundaries, component/path prediction, and reporting discipline.

### Modified Capabilities

- None.

## Impact

- Affected files are expected to stay under `skillset/user-plugins/gpu-analytical-modeling/` and this change directory.
- No Python APIs, CLI commands, packaged system skills, distribution manifests, or callback registry behavior should change.
- Validation should use skill-file inspection, local metadata checks, and the available skill validator for the touched skill directories.

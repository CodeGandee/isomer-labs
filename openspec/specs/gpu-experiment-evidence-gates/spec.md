# gpu-experiment-evidence-gates Specification

## Purpose
TBD - created by archiving change strengthen-gpu-experiment-evidence-gates. Update Purpose after archive.
## Requirements
### Requirement: Bottleneck Experiments Match Predictions to Observations
The GPU analytical-modeling Toolbox guidance SHALL require bottleneck-oriented experiments to connect each predicted saturated component or blocking path to an experiment that stresses one component or path at a time and collects hard evidence that supports or refutes the prediction.

#### Scenario: Targeted bottleneck experiment is required
- **WHEN** an agent designs or reviews an experiment for a model that predicts a saturated hardware component or blocking execution path
- **THEN** the guidance requires the agent to name the predicted component or path, choose an input or regime intended to stress that component or path, collect matching observational evidence, and report whether the observation supports, refutes, or leaves unresolved the prediction

#### Scenario: Coarse bottleneck labels are not enough
- **WHEN** the available experiment evidence only supports a broad label such as compute-bound or memory-bound
- **THEN** the guidance requires the agent to present that result as coarse support and avoid claiming exact component or path proof unless matching component/path observations are also shown

### Requirement: Analytical Latency Models Compare Predictions to Measurements
The GPU analytical-modeling Toolbox guidance SHALL require any proposed analytical model that predicts latency or runtime to compare predicted latency against measured latency under a declared workload and hardware scope before making latency-accuracy claims.

#### Scenario: Latency accuracy claim requires measurement
- **WHEN** an agent reports accuracy, error, fit quality, or validation for an analytical latency or runtime model
- **THEN** the guidance requires predicted latency, measured latency, measurement scope, metric definition, and evidence class to be stated together

#### Scenario: Proxy evidence cannot replace measured latency
- **WHEN** a model has only emulator, simulator, synthetic, analytical-proxy, or derivation-only evidence for latency
- **THEN** the guidance requires the agent to downgrade latency-accuracy language or route to measurement before claiming measured hardware accuracy

### Requirement: Final Reports Show Hard Evidence
The GPU analytical-modeling Toolbox guidance SHALL require final papers, reports, and closure summaries to show hard evidence for central runtime, saturated-component, and blocking-path claims rather than only stating conclusions.

#### Scenario: Central evidence is visible in final output
- **WHEN** an agent writes, reviews, or finalizes a paper, report, or closure summary for a GPU analytical model
- **THEN** the guidance requires the final output to show the relevant inputs, predictions, measured latency, observed bottleneck evidence, evidence mapping rationale, and match or mismatch interpretation for central claims

#### Scenario: Missing evidence blocks or limits closure
- **WHEN** central runtime, saturated-component, or blocking-path evidence is missing from the final output
- **THEN** the guidance requires the agent to route back to experiment, downgrade the claim, record an explicit limitation, or block publishable closure

### Requirement: Experiment Gate Guidance Remains Generic and Project-Local
The strengthened guidance SHALL remain generic to GPU kernel analytical modeling and project-local to the Toolbox directory.

#### Scenario: No runtime or distribution behavior changes
- **WHEN** the change is implemented
- **THEN** only `skillset/toolboxes/gpu-analytical-modeling/` and change artifacts are modified, with no edits to packaged system skills, callback registry behavior, CLI behavior, runtime behavior, or distribution manifests

#### Scenario: No topic-specific hard-coding
- **WHEN** the strengthened guidance uses examples
- **THEN** examples may name generic GPU evidence roles and hardware components but must not require a specific kernel, GPU SKU, topic workspace, host setup, command wrapper, profiler command, paper venue, paper artifact, or artifact path as general Toolbox context


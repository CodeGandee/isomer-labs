# gpu-analytical-modeling-skill-guidance Specification

## Purpose
TBD - created by archiving change strengthen-analytical-modeling-skills. Update Purpose after archive.
## Requirements
### Requirement: Analytical Model Shape Includes Execution Flow
The GPU analytical-modeling Toolbox guidance SHALL require an accepted GPU kernel analytical model to define an interpretable execution-flow shape that maps workload inputs through hardware components, ordered stages, and aggregation rules.

#### Scenario: Model-shape guidance names execution-flow artifacts
- **WHEN** an agent reads the strengthened modeling-method guidance for creating or evaluating a GPU analytical model
- **THEN** the guidance requires model inputs, model outputs, a hardware component graph, ordered execution stages, per-stage equations, aggregation logic, assumptions, and validity limits

#### Scenario: Coarse bandwidth model is insufficient
- **WHEN** a proposed model only uses a coarse compute-vs-memory or roofline-style bandwidth comparison for a claim about hardware execution flow
- **THEN** the guidance requires the agent to classify it as a baseline or incomplete model unless component/path equations and selection rules are also provided

### Requirement: Model Parameters Have Physical Meaning
The GPU analytical-modeling Toolbox guidance SHALL require analytical model parameters to have physical meanings, units or dimensions, sources or calibration roles, allowed ranges, and named effects on hardware components or execution paths.

#### Scenario: Anonymous fit factors are rejected
- **WHEN** a model introduces a coefficient, efficiency, factor, latency, bandwidth, probability, or threshold
- **THEN** the guidance requires the agent to name what physical behavior it represents, its units or dimensionless status, how it is sourced or calibrated, and what component or path it changes

#### Scenario: Calibration remains interpretable
- **WHEN** a model uses calibrated parameters
- **THEN** the guidance requires those parameters to be few, bounded, physically interpretable, and separated from held-out validation rather than treated as black-box fitting capacity

### Requirement: Execution-Flow Guidance Covers Data Movement and Ordering
The GPU analytical-modeling Toolbox guidance SHALL require execution-flow models to account for data slicing, per-hop movement between hardware components, ordering constraints, overlap, serialization, and pipeline behavior when those details affect the claimed runtime or bottleneck.

#### Scenario: Data movement is modeled as per-hop flow
- **WHEN** a model claims to explain memory, cache, transfer, or storage behavior
- **THEN** the guidance requires the agent to identify what data moves, how it is sliced or batched, which components it traverses, what cost applies to each hop, and which hops can overlap or serialize

#### Scenario: Pipeline and overlap rules are explicit
- **WHEN** a model aggregates stage times into runtime or bottleneck selection
- **THEN** the guidance requires explicit max, sum, overlap, queueing, recurrence, or piecewise rules rather than prose-only aggregation

### Requirement: Analytical Terms Prefer Closed-Form or Bounded Expressions
The GPU analytical-modeling Toolbox guidance SHALL prefer closed-form or bounded analytical expressions for model terms, while allowing stochastic, recurrence, queueing, or expectation-based terms when they are named, bounded, and justified.

#### Scenario: Stochastic behavior is represented explicitly
- **WHEN** a model includes inherently variable behavior such as cache misses, contention, scheduling effects, or reuse
- **THEN** the guidance requires an explicit probability, expectation, bound, calibration parameter, or uncertainty statement instead of an unnamed fudge factor

#### Scenario: Full simulator boundary is preserved
- **WHEN** an agent uses simulator-like language or simulator source material to shape a GPU model
- **THEN** the guidance requires the model to remain an analytical abstraction with bounded terms and source-backed assumptions rather than becoming an event-driven simulator or treating simulator output as target-hardware truth

### Requirement: Component and Path Selection Rules Are First-Class
The GPU analytical-modeling Toolbox guidance SHALL require models that claim bottleneck insight to define selection rules for saturated hardware component and blocking execution path, not only runtime.

#### Scenario: Bottleneck claim names a selection rule
- **WHEN** a model predicts a saturated component or blocking path
- **THEN** the guidance requires an explicit selection rule such as `argmax`, slack, active-cycle proxy, reservation time, dependency-chain cost, or critical-path rule

#### Scenario: Coarse labels are downgraded
- **WHEN** available model output or evidence only supports compute-bound versus memory-bound labels
- **THEN** the guidance requires the agent to present those labels as coarse support and avoid claiming exact component or path prediction

### Requirement: Bottleneck Predictions Are Verified Against Observations
The GPU analytical-modeling Toolbox guidance SHALL require bottleneck-oriented models to frame verification as predicted bottleneck component/path versus observed bottleneck evidence, not only predicted runtime versus measured runtime.

#### Scenario: Verification includes bottleneck observation
- **WHEN** a model claims it can identify bottlenecks or blocking paths
- **THEN** the guidance requires the agent to name what observation would support or refute each predicted component or path, such as counter trends, active-cycle evidence, instruction mix, dependency-chain evidence, microbenchmark behavior, or an explicit evidence gap

#### Scenario: Runtime accuracy alone is insufficient for bottleneck claims
- **WHEN** a model matches runtime but lacks evidence for its predicted saturated component or blocking path
- **THEN** the guidance requires the agent to classify the bottleneck explanation as unsupported or partially supported rather than validated

### Requirement: Strengthening Remains Project-Local and Generic
The strengthened guidance SHALL remain generic to GPU kernel analytical modeling and project-local to the Toolbox directory.

#### Scenario: No packaged skill or runtime behavior changes
- **WHEN** the change is implemented
- **THEN** only `skillset/toolboxes/gpu-analytical-modeling/` and change artifacts are modified, with no edits to packaged system skills, callback registry behavior, CLI behavior, or distribution manifests

#### Scenario: No topic-specific hard-coding
- **WHEN** the strengthened guidance uses examples
- **THEN** examples may name common GPU components but must not require a specific kernel, GPU SKU, private topic path, cross-host setup, paper artifact, host, environment setup, or topic-specific artifact as general Toolbox context


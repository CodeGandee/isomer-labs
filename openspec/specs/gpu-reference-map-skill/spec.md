# gpu-reference-map-skill Specification

## Purpose
TBD - created by archiving change add-gpu-reference-map-skill. Update Purpose after archive.
## Requirements
### Requirement: Reference Map Skill Centralizes Source Lookup
The GPU analytical-modeling user plugin SHALL provide a project-local `gpu-reference-map` callback skill that centralizes where agents should look for GPU analytical-modeling information and what each source family can justify.

#### Scenario: Source lookup has a dedicated entrance
- **WHEN** an agent needs sources for GPU analytical-modeling facts, parameters, execution-path structure, measurement evidence, simulator references, or literature
- **THEN** the plugin guidance directs the agent to `gpu-reference-map` rather than scattering detailed source taxonomy across operational skills

#### Scenario: Operational skills remain principle-focused
- **WHEN** an operational skill needs source guidance
- **THEN** it references `gpu-reference-map` for source families and limitations while retaining its own modeling, evidence, or reporting responsibilities

### Requirement: Reference Map Covers Required Source Families
The `gpu-reference-map` skill SHALL include maintainable command pages for local topic sources, kernel implementation sources, hardware documentation sources, profiler and counter sources, simulator architecture sources, measurement and microbenchmark sources, and literature sources.

#### Scenario: Source family command pages exist
- **WHEN** the reference-map skill is installed or inspected
- **THEN** each required source family is reachable from `gpu-reference-map/SKILL.md` through a command page

#### Scenario: Source family pages define use and limits
- **WHEN** an agent reads a source family command page
- **THEN** the page states where to look, what the source family can justify, what it cannot justify, and what metadata or caveats must be preserved

### Requirement: Simulator Sources Are Architecture References
The `gpu-reference-map` skill SHALL treat simulator projects such as AccelSim, GPGPU-Sim, and similar sources as architecture and execution-path references rather than direct target-hardware truth unless separately validated.

#### Scenario: Simulator reference is used for model structure
- **WHEN** an agent uses a simulator project to inform a GPU analytical model
- **THEN** the guidance allows architecture concepts, queues, schedulers, issue paths, memory partitions, and dependency-path abstractions while requiring target-hardware parameters and claims to come from source, measurement, or explicit assumption boundaries

### Requirement: Profiler and Counter Sources Preserve Raw Evidence
The `gpu-reference-map` skill SHALL describe profiler and counter sources as evidence sources that require raw metric names, command or collection context, normalization, counter-to-component mapping, and claim linkage.

#### Scenario: Counter source supports a bottleneck claim
- **WHEN** an agent uses profiler or counter evidence for a saturated-component or blocking-path claim
- **THEN** the guidance requires raw observations, mapping rationale, derived label separation, and support/refute/unresolved linkage to the model claim

### Requirement: Reference Map Is Registered as Project-Local Callback Guidance
The plugin manifest and README SHALL include `gpu-reference-map` as a project-local callback source for source-discovery and source-checking stages without changing packaged system skills or runtime behavior.

#### Scenario: Manifest includes reference-map callbacks
- **WHEN** an operator reads the plugin manifest
- **THEN** `gpu-reference-map` callback entries are available for stages where source lookup matters, such as scout, baseline, idea, analysis, experiment, or review

#### Scenario: Scope remains project-local
- **WHEN** this change is implemented
- **THEN** only `skillset/user-plugins/gpu-analytical-modeling/` and change artifacts are modified, with no edits to packaged system skills, callback registry behavior, CLI/runtime behavior, or distribution manifests

### Requirement: Reference Guidance Avoids Topic-Specific Hard-Coding
The reference-map skill SHALL remain generic to GPU kernel analytical modeling and SHALL NOT require a specific topic workspace, kernel, GPU SKU, host, paper venue, or artifact path as general plugin context.

#### Scenario: Examples remain source-class examples
- **WHEN** source pages use examples such as profiler tools, simulator projects, vendor documents, or modeling papers
- **THEN** examples identify source classes and limitations without turning one topic's tools, paths, targets, or paper workflow into a reusable requirement


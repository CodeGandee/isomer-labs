## MODIFIED Requirements

### Requirement: Reference Map Skill Centralizes Source Lookup
The GPU analytical-modeling Toolbox SHALL provide a project-local `gpu-reference-map` callback skill that centralizes where agents should look for GPU analytical-modeling information and what each source family can justify.

#### Scenario: Source lookup has a dedicated entrance
- **WHEN** an agent needs sources for GPU analytical-modeling facts, parameters, execution-path structure, measurement evidence, simulator references, or literature
- **THEN** the Toolbox guidance directs the agent to `gpu-reference-map` rather than scattering detailed source taxonomy across operational skills

#### Scenario: Operational skills remain principle-focused
- **WHEN** an operational skill needs source guidance
- **THEN** it references `gpu-reference-map` for source families and limitations while retaining its own modeling, evidence, or reporting responsibilities

### Requirement: Reference Map Is Registered as Project-Local Callback Guidance
The Toolbox manifest and README SHALL include `gpu-reference-map` as a project-local callback source for source-discovery and source-checking stages without changing packaged system skills.

#### Scenario: Manifest includes reference-map callbacks
- **WHEN** an operator reads the Toolbox manifest
- **THEN** `gpu-reference-map` callback entries are available for stages where source lookup matters, such as scout, baseline, idea, analysis, experiment, or review

#### Scenario: Scope remains project-local
- **WHEN** this change is implemented
- **THEN** GPU analytical modeling guidance lives under `skillset/toolboxes/gpu-analytical-modeling/`
- **AND** packaged system skills remain unchanged

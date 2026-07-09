## ADDED Requirements

### Requirement: GPU Analytical Modeling Toolbox Uses Stage-Prior Callback Prompts
The GPU analytical modeling Toolbox SHALL organize callback source material as stage-specific prior skills routed by short prompt-file callbacks.

#### Scenario: Callback prompt invokes installed prior skill
- **WHEN** a Toolbox callback entry targets a DeepSci insertion point
- **THEN** its prompt-file source names the `gpu-analytic-{stage}-prior` skill to invoke
- **AND** the prompt-file source names the specific subcommand and purpose for that insertion point

#### Scenario: Manifest is readable as stage-prior map
- **WHEN** an operator inspects `skillset/toolboxes/gpu-analytical-modeling/manifest.toml`
- **THEN** callback keys and descriptions identify the target DeepSci stage, callback timing, prior purpose, and prompt-file source

#### Scenario: Toolbox identity remains stable
- **WHEN** the stage-prior callback layout is used
- **THEN** the Toolbox manifest still uses `schema_version = "isomer-toolbox.v1"` and `toolbox_id = "gpu-analytical-modeling"`

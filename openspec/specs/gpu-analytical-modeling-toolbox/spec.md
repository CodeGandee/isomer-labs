# gpu-analytical-modeling-toolbox Specification

## Purpose
Define the project-local GPU analytical modeling Toolbox package and its durable schema.
## Requirements
### Requirement: GPU Analytical Modeling Toolbox Package
The GPU analytical modeling guidance SHALL live as a project-local Toolbox package under `skillset/toolboxes/gpu-analytical-modeling`.

#### Scenario: Toolbox package path is canonical
- **WHEN** an operator installs, inspects, documents, or validates the GPU analytical modeling package
- **THEN** the canonical path is `skillset/toolboxes/gpu-analytical-modeling`

#### Scenario: Toolbox manifest uses Toolbox schema
- **WHEN** the package manifest is read
- **THEN** it uses `schema_version = "isomer-toolbox.v1"` and `toolbox_id = "gpu-analytical-modeling"`

#### Scenario: README examples use Toolbox commands
- **WHEN** the package README shows installation or runtime parameter commands
- **THEN** it uses `project toolboxes`, `project toolbox-params`, and `project skill-callbacks install --toolbox-dir`

### Requirement: GPU Analytical Modeling Toolbox Remains Generic
The GPU analytical modeling Toolbox SHALL remain generic to GPU kernel analytical modeling and not require a specific topic workspace, kernel, GPU SKU, host, paper venue, or artifact path as reusable Toolbox context.

#### Scenario: No topic-specific hard-coding
- **WHEN** Toolbox instructions use examples
- **THEN** examples may name common GPU components, source classes, and evidence roles but must not require topic-specific paths, tools, targets, or paper workflows

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

### Requirement: GPU Analytical Modeling Toolbox Skills Declare Routed Manual Invocation
The GPU analytical modeling Toolbox SHALL mark its Toolbox prior skills as routed or manually invoked by default.

#### Scenario: Prior skills include non-implicit metadata
- **WHEN** the stage-prior skill directories under `skillset/toolboxes/gpu-analytical-modeling/` are inspected
- **THEN** each `gpu-analytic-*-prior` directory that contains `SKILL.md` also contains `agents/openai.yaml`
- **AND** that metadata sets `policy.allow_implicit_invocation` to `false`

#### Scenario: Prior skill prompts name routing posture
- **WHEN** a `gpu-analytic-*-prior/agents/openai.yaml` file is inspected
- **THEN** its default prompt describes the skill as used when routed by a Toolbox callback prompt or manually invoked
- **AND** it does not claim that the agent host should auto-select the prior implicitly

#### Scenario: Callback prompts remain explicit routers
- **WHEN** the GPU analytical modeling Toolbox callback prompt files are inspected
- **THEN** each prompt names the installed prior skill, subcommand, and purpose to invoke
- **AND** no callback prompt relies on silent automatic skill selection


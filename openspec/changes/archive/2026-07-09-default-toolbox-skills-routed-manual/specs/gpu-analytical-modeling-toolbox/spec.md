## ADDED Requirements

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

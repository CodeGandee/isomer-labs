## ADDED Requirements

### Requirement: Agent Env Setup Uses Package Specifics Only for Runtime Verification Caveats
The Agent Workspace environment setup service SHALL consume topic-level dependency planning as predecessor evidence and SHALL consult `isomer-misc-pkg-specifics` only when per-agent cwd readiness depends on package-specific runtime verification behavior.

#### Scenario: Missing topic package planning routes to topic env setup
- **WHEN** `derive-agent-env-gate` or `verify-agent-env-gate` needs package dependency planning that is absent, stale, or ambiguous in `topic.env.topic_setup_target_spec`
- **THEN** it reports a blocker and routes repair to `isomer-srv-topic-env-setup`
- **AND** it does not invent a separate per-agent package install plan

#### Scenario: Agent verification uses package-specific runtime checks
- **WHEN** a per-agent verification matrix item depends on a named package with package-specific runtime guidance
- **THEN** `isomer-srv-agent-env-setup` consults or consumes `isomer-misc-pkg-specifics` evidence for that package's runtime verification expectation
- **AND** it records the selected package-specific verification evidence or `no package-specific rule`

#### Scenario: Agent gate does not duplicate package source routing
- **WHEN** `derive-agent-env-gate` writes `topic.env.agent_setup_target_spec`
- **THEN** it references `topic.env.topic_setup_target_spec` for topic-level dependency and package-source decisions
- **AND** it does not write independent PyPI, Pixi, Conda, or runtime-wiring package install commands for dependencies that belong to topic env setup

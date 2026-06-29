## MODIFIED Requirements

### Requirement: Validation Distinguishes Topic and Agent Readiness Evidence
The Topic Team Specialization module skill SHALL validate topic environment readiness and Agent Workspace readiness as separate static setup evidence streams, and SHALL accept delegated environment readiness only when the required gate checklist evidence is complete.

#### Scenario: Topic env evidence cannot satisfy agent env evidence
- **WHEN** `validate-topic-team` or `finalize-topic-team` reads setup evidence
- **THEN** readiness from `isomer-srv-topic-env-setup` may satisfy only Topic Workspace environment setup evidence
- **AND** per-Agent Workspace cwd readiness requires `isomer-srv-agent-env-setup` evidence when that proof was requested

#### Scenario: Topic env ready requires complete topic checklist evidence
- **WHEN** `validate-topic-team` or `finalize-topic-team` consumes `isomer-srv-topic-env-setup` output that reports Topic Workspace environment readiness as `ready`
- **THEN** the operator evidence includes `topic.env.topic_setup_target_spec`, its `Gate Checklist`, and confirmation that every required checklist item is checked with supporting execution, path, dependency, resource, or expected-result evidence
- **AND** the operator does not treat topic env setup as ready when required checklist items are unchecked, missing, or completed only by a weaker smoke test that does not prove the named critical path

#### Scenario: Agent env ready requires complete per-agent checklist evidence
- **WHEN** `validate-topic-team` or `finalize-topic-team` consumes `isomer-srv-agent-env-setup` output that reports Agent Workspace environment readiness as `ready`
- **THEN** the operator evidence includes `topic.env.agent_setup_target_spec`, its `Gate Checklist`, readiness by Agent Name, and confirmation that every planned Agent Name has every required checklist item checked with supporting cwd execution, path, dependency, resource, projection, or expected-result evidence
- **AND** selected-agent partial evidence does not satisfy overall Agent Workspace environment readiness unless the complete planned Agent Name matrix has already passed

#### Scenario: Missing agent env proof is explicit
- **WHEN** per-Agent Workspace cwd verification was requested but `isomer-srv-agent-env-setup` evidence is missing
- **THEN** Topic Team Specialization reports an explicit blocker or not-checked status for Agent Workspace environment readiness
- **AND** it does not infer readiness from topic-root verification, Pixi install success, Git topology readiness, or selected-agent partial evidence

#### Scenario: Incomplete checklist item blocks static readiness
- **WHEN** delegated topic env or agent env evidence contains a required unchecked checklist item
- **THEN** `validate-topic-team` reports static setup readiness as blocked, failed, or not checked according to the delegated evidence
- **AND** it names the incomplete checklist item, owning target spec, reason, and next safe repair action

#### Scenario: Smoke-test downgrade remains visible
- **WHEN** delegated env setup evidence records that the user accepted a weaker smoke test instead of the original critical-path checklist item
- **THEN** `validate-topic-team` and `finalize-topic-team` preserve that limitation in validation and summary output
- **AND** they do not describe the weaker evidence as proof that the original critical path passed

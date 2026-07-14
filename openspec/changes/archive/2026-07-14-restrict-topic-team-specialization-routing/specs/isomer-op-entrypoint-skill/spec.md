## ADDED Requirements

### Requirement: Entrypoint Requires Agent Team Intent for Specialization
The operator entrypoint SHALL select `isomer-op-topic-team-specialize` only after the user explicitly invokes that skill or the prompt or authoritative Project context establishes a formal Agent Team target.

#### Scenario: Explicit specialization invocation is preserved
- **WHEN** the user explicitly invokes `isomer-op-topic-team-specialize`, `specialize-team`, or an equivalent named Agent Team specialization route
- **THEN** the entrypoint selects the Topic Team Specialization owner
- **AND** it preserves the supplied Research Topic and formal Agent Team context

#### Scenario: Prompt establishes Agent Team intent
- **WHEN** the user asks to deploy, specialize, instantiate, materialize, validate, repair, launch, or use an Agent Team and supplies or selects formal team context
- **THEN** the entrypoint may select `isomer-op-topic-team-specialize`
- **AND** its routing rationale names the Agent Team, Domain Agent Team Template, Topic Agent Team Profile, Topic Team Instantiation Packet, Agent Team Instance, or equivalent formal-team evidence

#### Scenario: Generic topic preparation does not imply a team
- **WHEN** the user asks to prepare, create, initialize, start, or repair a Research Topic without explicit or contextual formal Agent Team intent
- **THEN** the entrypoint routes new or partial setup to `isomer-op-topic-creator` and initialized-topic operations to `isomer-op-topic-mgr` or the applicable setup owner
- **AND** it does not select Topic Team Specialization from the topic name, Topic Workspace, generic readiness, missing summary, missing Agent Workspace, or generic launch-facing language alone

#### Scenario: Extension readiness recovery respects selected topology
- **WHEN** an extension workflow reports missing platform readiness
- **THEN** the entrypoint selects the owner of the missing base topic, actor, environment, runtime, or extension readiness layer
- **AND** it selects `isomer-op-topic-team-specialize` only when the selected topology already includes a formal Agent Team layer

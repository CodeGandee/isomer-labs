## ADDED Requirements

### Requirement: Topic Environment Setup Is a Protected Core Service
The core public pack SHALL preserve `isomer-srv-topic-env-setup` as protected service member `topic-env` without changing its Topic Workspace environment workflow.

#### Scenario: Protected Topic environment bundle exists
- **WHEN** core pack assets are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-srv-topic-env-setup/SKILL.md` exists
- **AND** its folder and frontmatter retain logical id `isomer-srv-topic-env-setup`

#### Scenario: Owner delegates environment setup
- **WHEN** an authorized operator or extension workflow needs Topic Workspace Pixi preparation or verification
- **THEN** it invokes `isomer-op-entrypoint->topic-env` or resolves the logical id for private projection
- **AND** the protected service preserves existing Gate, scope, path, and output requirements

#### Scenario: Service is not public
- **WHEN** ordinary host discovery or public core help is inspected
- **THEN** `isomer-srv-topic-env-setup` is not presented as an independent user entrypoint

#### Scenario: Logical owner remains stable
- **WHEN** a Service Request, Skill Binding Projection, or provenance record identifies the environment owner
- **THEN** it continues to use `isomer-srv-topic-env-setup`

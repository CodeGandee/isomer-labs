## MODIFIED Requirements

### Requirement: Topic Manager Skill Bundle
The core public pack SHALL preserve protected logical capability `isomer-op-topic-mgr` as member `topic-manage` for initialized Research Topic management after Topic Creator handoff.

#### Scenario: Topic Manager protected bundle exists
- **WHEN** the core pack is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-op-topic-mgr/SKILL.md` and `agents/openai.yaml`

#### Scenario: Topic Manager metadata is consistent
- **WHEN** the protected bundle is inspected
- **THEN** its folder and frontmatter retain logical id `isomer-op-topic-mgr`
- **AND** its metadata version is release-aligned and ordinary default guidance uses `$isomer-op-entrypoint use topic-manage to <task>`

#### Scenario: Topic Manager remains initialized-topic scoped
- **WHEN** its entrypoint describes purpose
- **THEN** it states that protected logical capability `isomer-op-topic-creator` owns initialization
- **AND** it owns initialized-topic storage, Topic Actors, team topology, environment mutation, verification, and diagnostics as before

#### Scenario: Public parent routes initialized-topic work
- **WHEN** a user asks to manage an initialized Research Topic
- **THEN** the public core entrypoint invokes `isomer-op-entrypoint->topic-manage`

### Requirement: Scope-Prefixed Command Structure
The protected Topic Manager SHALL retain its scope-prefixed routines under the parent-owned invocation designator.

#### Scenario: Internal command is invoked
- **WHEN** an active capability needs one Topic Manager routine
- **THEN** it invokes `isomer-op-entrypoint->topic-manage-><scope-command>()`
- **AND** the calling page declares the standard invocation notation

#### Scenario: User describes a scoped task
- **WHEN** a user asks the public core entrypoint for storage, actor, team, environment, or diagnostic work
- **THEN** the parent selects the matching protected Topic Manager command
- **AND** the user is not required to invoke the protected logical id directly

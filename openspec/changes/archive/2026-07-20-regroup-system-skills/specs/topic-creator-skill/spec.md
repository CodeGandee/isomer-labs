## MODIFIED Requirements

### Requirement: Topic Creator Operator Skill
The core public pack SHALL preserve protected logical capability `isomer-op-topic-creator` as member `topic-create` for taking empty or partial Project state to a manual-research-ready Topic Workspace.

#### Scenario: Topic Creator protected bundle exists
- **WHEN** the core pack is inspected
- **THEN** it contains `operator/isomer-op-entrypoint/subskills/isomer-op-topic-creator/SKILL.md` and `agents/openai.yaml`
- **AND** the folder and frontmatter retain logical id `isomer-op-topic-creator`
- **AND** its metadata version matches the package release

#### Scenario: Topic Creator is the protected initialization owner
- **WHEN** a user asks to create, initialize, prepare, or start a Research Topic from empty or partial Project state
- **THEN** `$isomer-op-entrypoint use topic-create to <task>` invokes `isomer-op-entrypoint->topic-create`
- **AND** the user does not need to know the protected Project Manager, Topic Manager, service, or research bootstrap sequence

#### Scenario: Protected identity remains durable
- **WHEN** a route, binding, callback, or provenance field names the Topic Creator owner
- **THEN** it uses logical id `isomer-op-topic-creator`
- **AND** runtime invocation resolves through the parent designator

### Requirement: Topic Creator Command Surface
The protected Topic Creator SHALL retain its bounded command surface while the public parent owns ordinary invocation.

#### Scenario: Public parent selects creation
- **WHEN** the user supplies a concrete Topic creation task
- **THEN** the parent routes it into the protected member's applicable subcommand
- **AND** it preserves existing clarification, Gate, service delegation, and finalize behavior

#### Scenario: Status explains progress
- **WHEN** the user invokes `status`
- **THEN** the skill reports which initialization stages are ready, blocked, skipped, or not started
- **AND** it names the next command that can advance the topic toward manual-research readiness

#### Scenario: Repair resumes from blockers
- **WHEN** the user invokes `repair` after a failed or partial topic initialization
- **THEN** the skill uses recorded state and Project Manifest-backed context to resume from the blocked stage
- **AND** it does not rerun already-ready destructive or expensive stages unless the user explicitly asks

#### Scenario: Internal command is named
- **WHEN** another protected workflow invokes a Topic Creator subcommand
- **THEN** it uses `isomer-op-entrypoint->topic-create-><command>()` and declares invocation notation

#### Scenario: Empty protected invocation occurs internally
- **WHEN** the protected member is invoked without a selected command
- **THEN** it uses its own help routine without becoming a top-level public skill

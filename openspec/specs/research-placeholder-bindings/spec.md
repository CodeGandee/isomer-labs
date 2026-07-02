# research-placeholder-bindings Specification

## Purpose
TBD - created by archiving change bind-research-v2-placeholders. Update Purpose after archive.
## Requirements
### Requirement: Skill Placeholder Binding Pages
The system SHALL provide a `placeholder-bindings.md` page for each active v2 research skill that defines `migrate/placeholders.md`.

#### Scenario: Binding page exists beside placeholder registry
- **WHEN** an active v2 research skill contains `migrate/placeholders.md`
- **THEN** the skill also contains `placeholder-bindings.md`

#### Scenario: Binding page preserves placeholder tokens
- **WHEN** `placeholder-bindings.md` lists a placeholder from `migrate/placeholders.md`
- **THEN** it preserves the exact placeholder token as metadata and does not replace it with a concrete path in workflow prose

#### Scenario: Binding page points to storage operations
- **WHEN** an agent needs to create, read, update, or archive a durable placeholder output
- **THEN** `placeholder-bindings.md` names the storage item class, default semantic label, artifact profile, and `isomer-cli ext research records` command shape to use

### Requirement: Placeholder Binding Coverage Validation
The system SHALL validate that active v2 placeholder binding pages cover the placeholders registered by each skill.

#### Scenario: Missing binding page is reported
- **WHEN** validation inspects an active v2 skill with `migrate/placeholders.md` and no `placeholder-bindings.md`
- **THEN** validation reports the missing binding page

#### Scenario: Missing placeholder binding is reported
- **WHEN** validation finds a placeholder in `migrate/placeholders.md` that is absent from `placeholder-bindings.md`
- **THEN** validation reports the unbound placeholder and the skill that owns it

#### Scenario: Extra placeholder binding is reported
- **WHEN** validation finds a placeholder in `placeholder-bindings.md` that is not registered in `migrate/placeholders.md`
- **THEN** validation reports the extra binding so migration drift can be repaired

### Requirement: Workspace Manager Binding Aggregation
The workspace manager skill SHALL treat local placeholder binding pages as the source material for the post-specialization binding registry.

#### Scenario: Workspace manager reads binding pages
- **WHEN** `isomer-rsch-workspace-mgr-v2` builds `<RSCH_PLACEHOLDER_BINDING_REGISTRY>`
- **THEN** it reads each relevant skill's `migrate/placeholders.md` and `placeholder-bindings.md`

#### Scenario: Binding registry records status
- **WHEN** a placeholder target is backed by implemented CLI support
- **THEN** the registry marks that binding available
- **AND** when support is planned, custom-needed, blocked, or deferred, the registry records that status instead of inventing an untracked path

### Requirement: Placeholder Bindings Use Global Isomer CLI
Active non-dev placeholder binding pages SHALL present record CRUD commands using the globally installed `isomer-cli` executable.

#### Scenario: Binding commands omit pixi prefix
- **WHEN** a non-dev `placeholder-bindings.md` row gives an `isomer-cli ext research records` create, list, show, update, or delete command
- **THEN** the command starts with `isomer-cli`
- **AND** it does not start with `pixi run isomer-cli`

#### Scenario: Binding metadata is preserved
- **WHEN** implementation removes the Pixi prefix from placeholder binding command rows
- **THEN** it preserves placeholders, record kinds, semantic labels, profiles, skill names, producer and consumer fields, metadata JSON, body flags, and content names


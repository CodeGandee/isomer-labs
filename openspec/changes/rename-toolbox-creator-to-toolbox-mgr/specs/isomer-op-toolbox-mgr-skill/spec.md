## ADDED Requirements

### Requirement: Toolbox Manager Skill Is Packaged Operator Guidance
The system SHALL provide `isomer-op-toolbox-mgr` as the packaged operator skill for creating and managing project-local Toolboxes through existing Isomer Toolbox, callback, Runtime Param, and path-safety surfaces.

#### Scenario: Manager skill asset exists
- **WHEN** packaged operator system skills are inspected
- **THEN** `operator/isomer-op-toolbox-mgr/SKILL.md` exists
- **AND** its frontmatter `name` is `isomer-op-toolbox-mgr`

#### Scenario: Creator skill asset is not active
- **WHEN** packaged operator system skills are inspected
- **THEN** `operator/isomer-op-toolbox-creator` is not listed as an active packaged skill path
- **AND** no packaged alias folder for `isomer-op-toolbox-creator` is required

#### Scenario: Manager naming matches responsibility
- **WHEN** the skill instructions and UI metadata are inspected
- **THEN** the title, frontmatter, display name, default prompt, help output, and operator catalog identify the skill as `isomer-op-toolbox-mgr`
- **AND** they describe creation as one part of broader Toolbox management

### Requirement: Toolbox Manager Skill Preserves Toolbox Command Surface
The rename SHALL preserve the existing Toolbox lifecycle command surface while changing the owning skill identity.

#### Scenario: Procedural subcommands remain available
- **WHEN** the manager skill subcommand table is inspected
- **THEN** it lists `author-toolbox`, `convert-skill`, `insert-callback`, `define-runtime-params`, `manage-toolbox`, and `identify-insertion-points`
- **AND** each procedural subcommand links to a local command page

#### Scenario: Helper subcommands remain grouped
- **WHEN** the manager skill helper table is inspected
- **THEN** it lists `author-toolbox-source`, `edit-callback-declarations`, `edit-runtime-params`, and `inspect-effective-state`
- **AND** CRUD-style operations for the same target resource remain grouped instead of split into separate helper subcommands

#### Scenario: Behavior stays CLI-backed
- **WHEN** the manager skill describes validation, install, callback refresh, Runtime Param mutation, or effective-state inspection
- **THEN** it continues to use existing `isomer-cli project toolboxes`, `project skill-callbacks`, and `project toolbox-params` command families
- **AND** it does not introduce new CLI or schema behavior

### Requirement: Toolbox Manager Skill Preserves Safety and Output Contracts
The rename SHALL preserve the safety, scope, and output requirements from the Toolbox management skill.

#### Scenario: Output contract remains available
- **WHEN** the manager skill completes an authoring, conversion, insertion, Runtime Param, management, or inspection task
- **THEN** it reports Essential Output by default
- **AND** Complete Output remains available on explicit request

#### Scenario: Scope and secret guardrails remain active
- **WHEN** the manager skill handles Toolbox scope, destructive operations, external paths, or secret-like material
- **THEN** it keeps explicit scope reporting, broad-effect warnings, path-safety blockers, and secret-hygiene blockers


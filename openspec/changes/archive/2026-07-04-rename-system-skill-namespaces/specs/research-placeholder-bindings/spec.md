## MODIFIED Requirements

### Requirement: Research Workspace Manager Binding Aggregation
The `isomer-deepsci-workspace-mgr` skill SHALL treat local placeholder binding pages as the source material for the post-specialization binding registry.

#### Scenario: Workspace manager reads binding pages
- **WHEN** `isomer-deepsci-workspace-mgr` builds `<RSCH_PLACEHOLDER_BINDING_REGISTRY>`
- **THEN** it reads each relevant skill's `migrate/placeholders.md` and `placeholder-bindings.md`

#### Scenario: Binding registry records status
- **WHEN** a placeholder target is backed by implemented CLI support
- **THEN** the registry marks that binding available
- **AND** when support is planned, custom-needed, blocked, or deferred, the registry records that status instead of inventing an untracked path

## ADDED Requirements

### Requirement: Placeholder Binding Metadata Uses Active DeepSci Names
Active production DeepSci placeholder binding pages SHALL use `isomer-deepsci-*` skill names in binding metadata and example commands.

#### Scenario: Binding command skill flag uses DeepSci namespace
- **WHEN** a non-dev `placeholder-bindings.md` row gives an `isomer-cli ext research records` create, list, show, update, or delete command for a production DeepSci skill
- **THEN** the command uses the active `isomer-deepsci-<purpose>` value in `--skill`
- **AND** it does not use an old `isomer-rsch-<purpose>` value

#### Scenario: Producer and consumer metadata uses active DeepSci namespace
- **WHEN** a binding row names producer or consumer skill fields for production DeepSci skills
- **THEN** those fields use `isomer-deepsci-*` names for skill-specific producers and consumers
- **AND** historical `isomer-rsch-*` names appear only in passive provenance or migration context

## MODIFIED Requirements

### Requirement: Toolbox Registration CRUD
The system SHALL expose Toolbox registrations as project CLI resources that can be installed as effective Toolbox bundles, listed, shown, explained, enabled, disabled, source-updated, uninstalled, and validated without editing packaged system skill assets.

#### Scenario: Toolbox install records project bundle
- **WHEN** a user runs `isomer-cli project toolboxes install --toolbox-dir <path>` without a Research Topic selector
- **THEN** the system validates the Toolbox manifest, writes or updates a Project Manifest `[[toolboxes]]` row with `scope = "project"`, installs declared Toolbox callback records at Project scope, applies the documented runtime-param default import policy for Project scope, and reports the Toolbox id, source path, status, scope, installed callbacks, runtime-param import status, effective status, and diagnostics

#### Scenario: Toolbox install derives id from manifest
- **WHEN** a user runs `isomer-cli project toolboxes install --toolbox-dir <path>`
- **THEN** the command reads `toolbox_id` from the Toolbox manifest
- **AND** the command does not take a positional Toolbox id argument

#### Scenario: Toolbox install records topic bundle
- **WHEN** a user runs `isomer-cli project toolboxes install --toolbox-dir <path> --topic <topic-id>`
- **THEN** the system validates the Toolbox manifest, writes or updates a Topic Workspace Manifest `[[toolboxes]]` row with `scope = "research_topic"`, installs declared Toolbox callback records at Research Topic scope, applies the documented runtime-param default import policy for the Topic Workspace scope, and reports the Toolbox id, source path, status, scope, selected Research Topic, installed callbacks, runtime-param import status, effective status, and diagnostics

#### Scenario: Toolbox install preserves lower-level configuration
- **WHEN** a Toolbox install refreshes callback records or registration metadata for one Toolbox and selected scope
- **THEN** the system preserves runtime params, runtime-param imports, callback records for other Toolboxes, and Toolbox registrations for other scopes

#### Scenario: Toolbox enablement is scope-specific
- **WHEN** a user enables or disables a Toolbox with Project, Research Topic, Topic Actor, or Topic Agent selectors
- **THEN** the system writes only the selected scope layer and does not delete broader or narrower Toolbox registrations

#### Scenario: Toolbox uninstall removes selected layer only
- **WHEN** a user uninstalls a Toolbox with a selected scope
- **THEN** the system removes or archives only that scope's `[[toolboxes]]` row and leaves callback records, runtime params, imports, and other scope registrations untouched

#### Scenario: Toolbox install reports narrower scope boundary
- **WHEN** a user selects Topic Actor or Topic Agent scope for Toolbox installation while the Toolbox declares callbacks
- **THEN** the system reports whether callback records are installed at the containing Research Topic scope or rejected because callback storage does not support the narrower scope
- **AND** the system keeps Topic Actor or Topic Agent scope available for Toolbox status and runtime-param configuration where supported

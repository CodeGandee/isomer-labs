## MODIFIED Requirements

### Requirement: Toolbox Callback Install Semantics
The system SHALL install Toolbox callback manifest entries by upserting the installed callback key rather than replacing all callbacks for an extension point, and SHALL support both high-level Toolbox bundle installation and lower-level callback-manifest installation.

#### Scenario: Toolbox bundle install materializes callbacks
- **WHEN** a user installs a Toolbox bundle through `isomer-cli project toolboxes install --toolbox-dir <path>`
- **THEN** the system installs the Toolbox manifest callback entries into the selected callback registry scope as part of the bundle operation

#### Scenario: Callback manifest primitive remains available
- **WHEN** a user invokes the lower-level callback-manifest install operation for a Toolbox directory
- **THEN** the system refreshes callback records from that Toolbox manifest without requiring runtime-param default imports to be installed
- **AND** the operation is valid for migration, repair, test setup, and not-yet-fully-orchestrated callback bundle workflows

#### Scenario: Toolbox manifest kind is canonical
- **WHEN** a Toolbox callback manifest is loaded
- **THEN** the system requires `kind = "toolbox-callback-bundle"`

#### Scenario: Same installed key updates one callback
- **WHEN** a Toolbox callback install operation writes a callback whose installed callback key already exists in the selected registry scope
- **THEN** the system updates that callback record
- **AND** the system does not remove other callback records for the same `target_skill` and `stage`

#### Scenario: Same extension point from different Toolboxes coexists
- **WHEN** two Toolboxes install callbacks for the same `target_skill` and `stage`
- **THEN** the installed callback keys differ by `toolbox_id`
- **AND** both callback records remain visible to User Skill Callback resolution

#### Scenario: Toolbox metadata is stored with installed callback
- **WHEN** the system installs a callback from a Toolbox manifest
- **THEN** the registry record includes the installed callback key
- **AND** the registry record includes the source `toolbox_id` and toolbox-local callback key as metadata

#### Scenario: Different source with same Toolbox id requires replace
- **WHEN** the system installs a Toolbox manifest whose `toolbox_id` matches an already installed Toolbox from a different source identity
- **THEN** installation is rejected unless the user explicitly requests replacement

### Requirement: Callback Install Ensures Toolbox Registration
Installing callbacks from a Toolbox manifest SHALL ensure the Toolbox is registered at the same selected scope, whether callback installation is reached through high-level Toolbox bundle installation or the lower-level callback-manifest primitive.

#### Scenario: Callback install creates Toolbox registration
- **WHEN** callback installation processes a Toolbox manifest for a scope that has no matching `[[toolboxes]]` row
- **THEN** the system writes a Toolbox registration for the manifest `toolbox_id`, source path, selected scope, and active status before reporting install success

#### Scenario: Callback install updates matching Toolbox registration
- **WHEN** callback installation processes a Toolbox manifest for a scope that already has a matching Toolbox registration from the same source
- **THEN** the system preserves existing Toolbox runtime params and imports while refreshing callback records and compatible Toolbox registration metadata

#### Scenario: Callback install does not delete Toolbox configuration
- **WHEN** callback installation updates or replaces callbacks for a Toolbox
- **THEN** the system does not delete runtime param rows, runtime param import rows, or Toolbox registrations for other scopes

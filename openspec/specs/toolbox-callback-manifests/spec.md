# toolbox-callback-manifests Specification

## Purpose
Define Toolbox callback manifests, installed callback key namespacing, install semantics, and Toolbox manifest runtime declarations.
## Requirements
### Requirement: Toolbox Callback Key Contract
The system SHALL derive every installed callback key from a required Toolbox `toolbox_id` and a toolbox-local callback key.

#### Scenario: Toolbox id is explicit
- **WHEN** a Toolbox callback manifest is loaded
- **THEN** the system requires a non-empty `toolbox_id` field as the stable Toolbox identity string
- **AND** the system does not treat a broad top-level `id` field as the Toolbox identity

#### Scenario: Explicit callback key is toolbox-local
- **WHEN** a Toolbox manifest callback entry sets `key`
- **THEN** the system uses that string as the toolbox-local callback key for that entry

#### Scenario: Callback id is not a key alias
- **WHEN** a Toolbox manifest callback entry sets `id` instead of `key`
- **THEN** manifest validation rejects the entry with a deterministic diagnostic that asks for `key`

#### Scenario: Toolbox-local key character set is bounded
- **WHEN** the system validates a toolbox-local callback key
- **THEN** validation accepts only ASCII letters, ASCII digits, `-`, `_`, and `/`
- **AND** validation rejects keys containing `.`, `:`, whitespace, or other characters

#### Scenario: Installed callback key is namespaced by Toolbox
- **WHEN** the system prepares a manifest callback entry for installation
- **THEN** the installed callback key is `<toolbox_id>:<toolbox-local-key>`
- **AND** the installed callback key is the callback id stored in the User Skill Callback registry

#### Scenario: Toolbox authors manage only local uniqueness
- **WHEN** two different Toolboxes declare the same toolbox-local callback key
- **THEN** the installed callback keys remain distinct because each key is prefixed with its `toolbox_id`

#### Scenario: Duplicate local key is rejected inside one Toolbox
- **WHEN** one Toolbox manifest contains two callback entries with the same effective toolbox-local callback key
- **THEN** manifest validation rejects the Toolbox with a deterministic diagnostic before installation writes callback registry records

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

### Requirement: Toolbox Runtime Param Manifest Declarations
Toolbox callback manifests SHALL optionally declare runtime parameter definitions and default parameter bundles without making those declarations installed project configuration by themselves.

#### Scenario: Manifest declares runtime param definitions
- **WHEN** a Toolbox manifest includes `[[runtime_params]]` entries
- **THEN** validation accepts entries that define toolbox-local param keys, value types, allowed values when required, defaults, descriptions, and statuses for that Toolbox id

#### Scenario: Manifest param keys are toolbox-local
- **WHEN** a Toolbox manifest runtime param entry sets `key`
- **THEN** the system treats the key as toolbox-local and derives the effective param id as `<toolbox_id>:<key>`

#### Scenario: Manifest declares default param import bundles
- **WHEN** a Toolbox manifest declares named runtime param default bundles
- **THEN** the system validates that each bundle path is relative to the Toolbox root, resolves inside the Toolbox directory, and points to a readable TOML file containing runtime param rows

#### Scenario: Manifest declarations do not write user config
- **WHEN** a Toolbox manifest declares runtime params or default bundles
- **THEN** loading the manifest does not write the Project Manifest, Topic Workspace Manifest, callback registry, or import files unless a user invokes an explicit install, define, set, or import command

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

### Requirement: Toolbox Callback Targets Use Insertion Point Catalog
Toolbox callback manifest validation SHALL validate each callback target skill and stage pair against manifest-declared callback insertion points.

#### Scenario: Toolbox callback targets declared insertion point
- **WHEN** a Toolbox callback manifest entry targets a system skill and stage pair declared in the packaged callback insertion-point catalog
- **THEN** manifest validation accepts the target pair subject to existing Toolbox callback key, source, path, and duplicate-key rules

#### Scenario: Toolbox callback targets undeclared insertion point
- **WHEN** a Toolbox callback manifest entry targets a packaged system skill and stage pair that is not declared as a callback insertion point
- **THEN** manifest validation rejects the entry with a deterministic diagnostic that names the missing insertion point

#### Scenario: Optional extension target does not require filesystem verification
- **WHEN** a Toolbox callback manifest entry targets a known optional system extension insertion point
- **THEN** validation uses the packaged callback insertion-point catalog and does not inspect Project operator skill files


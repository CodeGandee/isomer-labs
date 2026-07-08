## REMOVED Requirements

### Requirement: Callback Keys Support User Plugin Namespaces
**Reason**: Callback namespace support now uses Toolbox identity and toolbox-local keys.
**Migration**: Use the added `Callback Keys Support Toolbox Namespaces` requirement.

### Requirement: Plugin Status Gates Plugin-Installed Callbacks
**Reason**: Callback gating now uses effective Toolbox status for callbacks installed from Toolbox manifests.
**Migration**: Use the added `Toolbox Status Gates Toolbox-Installed Callbacks` requirement.

## ADDED Requirements

### Requirement: Callback Keys Support Toolbox Namespaces
The system SHALL accept callback ids that include a Toolbox namespace separator so installed Toolbox callbacks can use `<toolbox_id>:<toolbox-local-key>` as their stable callback key.

#### Scenario: Namespaced callback key is valid
- **WHEN** callback validation sees an installed callback key in the form `<toolbox_id>:<toolbox-local-key>`
- **THEN** validation accepts exactly one colon namespace separator when the Toolbox id and toolbox-local key otherwise use valid callback key characters

#### Scenario: Toolbox-local part cannot contain colon
- **WHEN** callback validation sees an installed callback key whose toolbox-local key part contains `:`
- **THEN** validation rejects the callback key with a deterministic diagnostic

#### Scenario: Duplicate active namespaced keys are rejected
- **WHEN** two active callback records visible to a Project or Research Topic context use the same installed callback key
- **THEN** validation rejects the duplicate active callback key with a deterministic diagnostic

#### Scenario: Registry output preserves installed callback key
- **WHEN** the system lists, shows, resolves, disables, validates, or serializes a callback installed from a Toolbox manifest
- **THEN** the reported callback id is the installed callback key

#### Scenario: Toolbox metadata is optional for manual callbacks
- **WHEN** a callback is registered directly without a Toolbox manifest
- **THEN** the registry record does not require `toolbox_id` or toolbox-local callback key metadata

### Requirement: Toolbox Status Gates Toolbox-Installed Callbacks
The system SHALL honor effective Toolbox status when resolving callbacks installed from Toolbox manifests.

#### Scenario: Active Toolbox callback resolves normally
- **WHEN** an active callback record has `toolbox_id` metadata and the effective Toolbox status for the selected Project, Research Topic, Topic Actor, or Topic Agent context is `active`
- **THEN** callback resolution may include that callback when its target skill and stage match the request

#### Scenario: Disabled Toolbox callback is skipped
- **WHEN** an active callback record has `toolbox_id` metadata and the effective Toolbox status for the selected context is disabled
- **THEN** callback resolution excludes that callback without deleting or mutating the callback registry record

#### Scenario: Missing Toolbox registration blocks installed callback
- **WHEN** an active callback record has `toolbox_id` metadata but no applicable Toolbox registration exists
- **THEN** callback resolution excludes that callback with a deterministic diagnostic

#### Scenario: Disablement is context-specific
- **WHEN** a Toolbox is disabled for one Topic Actor or Topic Agent but remains enabled at the broader Research Topic or Project scope
- **THEN** callback resolution skips the Toolbox callbacks only for the disabled effective context and continues resolving them for other contexts where the Toolbox remains enabled

#### Scenario: Callback list explains Toolbox gating
- **WHEN** a callback list, resolve, show, or validate command reports Toolbox-installed callbacks
- **THEN** the output includes enough Toolbox status metadata to explain whether the callback is effective or gated off for the selected context

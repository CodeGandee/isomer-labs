## ADDED Requirements

### Requirement: Callback Keys Support User Plugin Namespaces
The system SHALL accept callback ids that include a user-plugin namespace separator so installed user-plugin callbacks can use `<plugin-name>:<plugin-local-key>` as their stable callback key, where `<plugin-name>` is the stable plugin identity string.

#### Scenario: Namespaced callback key is valid
- **WHEN** callback validation sees an installed callback key in the form `<plugin-name>:<plugin-local-key>`
- **THEN** validation accepts the colon namespace separator when the plugin name and plugin-local key otherwise use valid callback key characters

#### Scenario: Duplicate active namespaced keys are rejected
- **WHEN** two active callback records visible to a Project or Research Topic context use the same installed callback key
- **THEN** validation rejects the duplicate active callback key with a deterministic diagnostic

#### Scenario: Distinct namespaced keys coexist on one extension point
- **WHEN** two active callback records have the same target system skill name and callback stage but different installed callback keys
- **THEN** callback resolution includes both records

#### Scenario: Extension point does not overwrite callback identity
- **WHEN** a callback registration or plugin install writes a callback for a target system skill name and callback stage that already has another callback
- **THEN** the existing callback remains registered unless its installed callback key is the same as the new callback key

#### Scenario: Registry output preserves installed callback key
- **WHEN** the system lists, shows, resolves, disables, validates, or serializes a callback installed from a user-plugin manifest
- **THEN** the reported callback id is the installed callback key

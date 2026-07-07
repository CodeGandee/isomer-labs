## ADDED Requirements

### Requirement: User Plugin Callback Key Contract
The system SHALL derive every installed callback key from a stable user-plugin identity string and a plugin-local callback key.

#### Scenario: Explicit callback key is plugin-local
- **WHEN** a user-plugin manifest callback entry sets `key`
- **THEN** the system uses that string as the plugin-local callback key for that entry

#### Scenario: Missing callback key derives from extension point
- **WHEN** a user-plugin manifest callback entry does not set `key`
- **THEN** the system derives the plugin-local callback key from the canonical extension point name
- **AND** the initial canonical extension point name is `<target_skill>.<stage>`

#### Scenario: Installed callback key is namespaced by plugin
- **WHEN** the system prepares a manifest callback entry for installation
- **THEN** the installed callback key is `<plugin-name>:<plugin-local-key>`
- **AND** the installed callback key is the callback id stored in the User Skill Callback registry

#### Scenario: Plugin name uses stable identity
- **WHEN** the system derives an installed callback key from a user-plugin manifest
- **THEN** `<plugin-name>` is the plugin's stable identity string rather than its human display name

#### Scenario: Plugin authors manage only local uniqueness
- **WHEN** two different user plugins declare the same plugin-local callback key
- **THEN** the installed callback keys remain distinct because each key is prefixed with its plugin name

#### Scenario: Duplicate local key is rejected inside one plugin
- **WHEN** one user-plugin manifest contains two callback entries with the same effective plugin-local callback key
- **THEN** manifest validation rejects the plugin with a deterministic diagnostic before installation writes callback registry records

#### Scenario: Unlabeled duplicate extension point is rejected
- **WHEN** one user-plugin manifest contains two callback entries for the same `target_skill` and `stage` and neither entry sets `key`
- **THEN** both entries derive the same plugin-local callback key
- **AND** manifest validation rejects the plugin unless the entries are given distinct explicit keys

#### Scenario: Explicit keys allow multiple callbacks on one extension point
- **WHEN** one user-plugin manifest contains multiple callback entries for the same `target_skill` and `stage` with distinct explicit keys
- **THEN** manifest validation accepts those entries as distinct callbacks for the same extension point

### Requirement: User Plugin Callback Install Semantics
The system SHALL install user-plugin callback manifest entries by upserting the installed callback key rather than replacing all callbacks for an extension point.

#### Scenario: Same installed key updates one callback
- **WHEN** a user-plugin callback install operation writes a callback whose installed callback key already exists in the selected registry scope
- **THEN** the system updates that callback record
- **AND** the system does not remove other callback records for the same `target_skill` and `stage`

#### Scenario: Same extension point from different plugins coexists
- **WHEN** two user plugins install callbacks for the same `target_skill` and `stage`
- **THEN** the installed callback keys differ by plugin name
- **AND** both callback records remain visible to User Skill Callback resolution

#### Scenario: Same extension point from one plugin with distinct keys coexists
- **WHEN** one user plugin installs two callbacks for the same `target_skill` and `stage` with distinct plugin-local keys
- **THEN** both callback records remain visible to User Skill Callback resolution

#### Scenario: Extension point is not the registry identity
- **WHEN** a callback registry already contains a callback for a `target_skill` and `stage`
- **THEN** installing another callback for that same `target_skill` and `stage` does not overwrite the existing record unless the installed callback key is identical

### Requirement: User Plugin Callback Ordering
The system SHALL expose user-facing ordering guarantees for callbacks from the same plugin only, using ascending Python string comparison on plugin-local callback keys.

#### Scenario: In-plugin callback order uses Python string comparison
- **WHEN** multiple callbacks from the same user plugin apply to the same extension point
- **THEN** the user-facing order for those callbacks is ascending Python `str` comparison of their plugin-local callback keys

#### Scenario: Cross-plugin callback order is not user-facing
- **WHEN** callbacks from multiple user plugins apply to the same extension point
- **THEN** the system does not expose a user-facing guarantee that one plugin's callback runs before another plugin's callback

#### Scenario: Cross-plugin output can remain deterministic
- **WHEN** the system lists, validates, installs, or resolves callbacks from multiple user plugins
- **THEN** the implementation may use a deterministic order for reproducible output
- **AND** that cross-plugin order is treated as an implementation detail

#### Scenario: Manifest priority does not define plugin order
- **WHEN** a user-plugin manifest includes callback entries with numeric priority fields or physical file order
- **THEN** those values do not define the user-facing order between callbacks from the same plugin

## ADDED Requirements

### Requirement: User Plugin Callback Key Contract
The system SHALL derive every installed callback key from a required user-plugin `plugin_id` and a plugin-local callback key.

#### Scenario: Plugin id is explicit
- **WHEN** a user-plugin callback manifest is loaded
- **THEN** the system requires a non-empty `plugin_id` field as the stable plugin identity string
- **AND** the system does not treat a broad top-level `id` field as the plugin identity

#### Scenario: Explicit callback key is plugin-local
- **WHEN** a user-plugin manifest callback entry sets `key`
- **THEN** the system uses that string as the plugin-local callback key for that entry

#### Scenario: Callback id is not a key alias
- **WHEN** a user-plugin manifest callback entry sets `id` instead of `key`
- **THEN** manifest validation rejects the entry with a deterministic diagnostic that asks for `key`

#### Scenario: Plugin-local key character set is bounded
- **WHEN** the system validates a plugin-local callback key
- **THEN** validation accepts only ASCII letters, ASCII digits, `-`, `_`, and `/`
- **AND** validation rejects keys containing `.`, `:`, whitespace, or other characters

#### Scenario: Slash is only naming hierarchy
- **WHEN** a plugin-local callback key contains `/`
- **THEN** the system treats `/` as part of the key string for naming hierarchy
- **AND** the system does not interpret `/` as a filesystem path separator, dependency edge, or ordering rule

#### Scenario: Missing callback key derives from extension point
- **WHEN** a user-plugin manifest callback entry does not set `key`
- **THEN** the system derives the plugin-local callback key from the canonical extension point name
- **AND** the initial canonical extension point name is `<target_skill>/<stage>`

#### Scenario: Installed callback key is namespaced by plugin
- **WHEN** the system prepares a manifest callback entry for installation
- **THEN** the installed callback key is `<plugin_id>:<plugin-local-key>`
- **AND** the installed callback key is the callback id stored in the User Skill Callback registry

#### Scenario: Plugin authors manage only local uniqueness
- **WHEN** two different user plugins declare the same plugin-local callback key
- **THEN** the installed callback keys remain distinct because each key is prefixed with its `plugin_id`

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

#### Scenario: Plugin install command is callback-scoped
- **WHEN** a user installs a user-plugin callback manifest
- **THEN** the CLI command is `isomer-cli project skill-callbacks install --plugin-dir <path>`

#### Scenario: Same installed key updates one callback
- **WHEN** a user-plugin callback install operation writes a callback whose installed callback key already exists in the selected registry scope
- **THEN** the system updates that callback record
- **AND** the system does not remove other callback records for the same `target_skill` and `stage`

#### Scenario: Same extension point from different plugins coexists
- **WHEN** two user plugins install callbacks for the same `target_skill` and `stage`
- **THEN** the installed callback keys differ by `plugin_id`
- **AND** both callback records remain visible to User Skill Callback resolution

#### Scenario: Same extension point from one plugin with distinct keys coexists
- **WHEN** one user plugin installs two callbacks for the same `target_skill` and `stage` with distinct plugin-local keys
- **THEN** both callback records remain visible to User Skill Callback resolution

#### Scenario: Extension point is not the registry identity
- **WHEN** a callback registry already contains a callback for a `target_skill` and `stage`
- **THEN** installing another callback for that same `target_skill` and `stage` does not overwrite the existing record unless the installed callback key is identical

#### Scenario: Plugin-installed callbacks use equal priority
- **WHEN** the system installs callbacks from a user-plugin manifest
- **THEN** each installed callback uses the same callback priority value for that registry scope
- **AND** manifest callback priority fields do not change plugin-installed callback ordering

#### Scenario: Plugin metadata is stored with installed callback
- **WHEN** the system installs a callback from a user-plugin manifest
- **THEN** the registry record includes the installed callback key
- **AND** the registry record includes the source `plugin_id` and plugin-local callback key as metadata

#### Scenario: Different source with same plugin id requires replace
- **WHEN** the system installs a user-plugin manifest whose `plugin_id` matches an already installed plugin from a different source identity
- **THEN** installation is rejected unless the user explicitly requests replacement

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

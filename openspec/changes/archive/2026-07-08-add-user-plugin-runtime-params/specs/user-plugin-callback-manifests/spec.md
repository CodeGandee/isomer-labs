## ADDED Requirements

### Requirement: User Plugin Runtime Param Manifest Declarations
User-plugin callback manifests SHALL optionally declare runtime param definitions and default param bundles without making those declarations installed project configuration by themselves.

#### Scenario: Manifest declares runtime param definitions
- **WHEN** a user-plugin manifest includes `[[runtime_params]]` entries
- **THEN** validation accepts entries that define plugin-local param keys, value types, allowed values when required, defaults, descriptions, and statuses for that plugin id

#### Scenario: Manifest param keys are plugin-local
- **WHEN** a user-plugin manifest runtime param entry sets `key`
- **THEN** the system treats the key as plugin-local and derives the effective param id as `<plugin_id>:<key>`

#### Scenario: Manifest declares default param import bundles
- **WHEN** a user-plugin manifest declares named runtime param default bundles
- **THEN** the system validates that each bundle path is relative to the plugin root, resolves inside the plugin directory, and points to a readable TOML file containing runtime param rows

#### Scenario: Manifest declarations do not write user config
- **WHEN** a user-plugin manifest declares runtime params or default bundles
- **THEN** loading the manifest does not write the Project Manifest, Topic Workspace Manifest, callback registry, or import files unless a user invokes an explicit install, define, set, or import command

#### Scenario: Runtime params are optional for callback bundles
- **WHEN** an existing user-plugin callback manifest contains callback entries and no runtime param declarations
- **THEN** manifest validation keeps accepting the plugin as a callback bundle

### Requirement: Callback Install Ensures User Plugin Registration
Installing callbacks from a user-plugin manifest SHALL ensure the plugin is registered as a User Plugin at the same selected scope.

#### Scenario: Callback install creates plugin registration
- **WHEN** a user runs `isomer-cli project skill-callbacks install --plugin-dir <path>` for a scope that has no matching `[[user_plugins]]` row
- **THEN** the system writes a User Plugin registration for the manifest `plugin_id`, source path, selected scope, and active status before reporting install success

#### Scenario: Callback install updates matching plugin registration
- **WHEN** a user runs callback install for a scope that already has a matching User Plugin registration from the same source
- **THEN** the system preserves existing plugin runtime params and imports while refreshing callback records and compatible plugin registration metadata

#### Scenario: Callback install does not delete plugin configuration
- **WHEN** callback install updates or replaces callbacks for a plugin
- **THEN** the system does not delete runtime param rows, runtime param import rows, or plugin registrations for other scopes

# user-plugin-runtime-configuration Specification

## Purpose
Define User Plugin registration and runtime-param configuration across Project Manifest and Topic Workspace Manifest layers.

## Requirements
### Requirement: User Plugin Registration CRUD
The system SHALL expose User Plugin registrations as project CLI resources that can be installed, listed, shown, explained, enabled, disabled, source-updated, uninstalled, and validated without editing packaged system skill assets.

#### Scenario: Plugin install records project registration
- **WHEN** a user runs `isomer-cli project user-plugins install --plugin-dir <path>` without a Research Topic selector
- **THEN** the system validates the plugin manifest, writes or updates a Project Manifest `[[user_plugins]]` row with `scope = "project"`, and reports the plugin id, source path, status, scope, and diagnostics

#### Scenario: Callback install records plugin registration
- **WHEN** a user runs `isomer-cli project skill-callbacks install --plugin-dir <path>` with Project or topic selectors
- **THEN** the system ensures a matching `[[user_plugins]]` registration exists at the same selected scope
- **AND** it preserves runtime params, imports, callback records for other plugins, and plugin registrations for other scopes

#### Scenario: Plugin install records topic registration
- **WHEN** a user runs `isomer-cli project user-plugins install --plugin-dir <path> --topic <topic-id>`
- **THEN** the system validates the plugin manifest, writes or updates a Topic Workspace Manifest `[[user_plugins]]` row with `scope = "research_topic"`, and reports the plugin id, source path, status, scope, selected Research Topic, and diagnostics

#### Scenario: Plugin enablement is scope-specific
- **WHEN** a user enables or disables a User Plugin with Project, Research Topic, Topic Actor, or Topic Agent selectors
- **THEN** the system writes only the selected scope layer and does not delete broader or narrower plugin registrations

#### Scenario: Plugin status vocabulary is bounded
- **WHEN** validation reads a User Plugin registration status
- **THEN** it accepts only `active` and `disabled`
- **AND** it rejects `enabled`, `inactive`, and other status spellings for User Plugin registrations

#### Scenario: Plugin uninstall removes selected layer only
- **WHEN** a user uninstalls a User Plugin with a selected scope
- **THEN** the system removes or archives only that scope's `[[user_plugins]]` row and leaves callback records, runtime params, imports, and other scope registrations untouched

#### Scenario: Plugin explain reports status stack
- **WHEN** a user runs `isomer-cli --print-json project user-plugins explain <plugin-id>` with optional topic, Topic Actor, or Topic Agent selectors
- **THEN** the output includes every applicable plugin status candidate, its source file, selected effective status, and whether each candidate was overridden

### Requirement: Runtime Param Table Schema
The system SHALL represent plugin-specific runtime params with `[[user_plugin_runtime_params]]` tables that use the same authoring shape in Project Manifests, Topic Workspace Manifests, and param import files.

#### Scenario: Project Manifest accepts project params
- **WHEN** the Project Manifest contains a `[[user_plugin_runtime_params]]` row
- **THEN** validation accepts the row only when `scope = "project"` or the scope is omitted and defaults to `project`

#### Scenario: Project Manifest rejects topic-local params
- **WHEN** the Project Manifest contains a runtime param row with `scope = "research_topic"`, `scope = "topic_actor"`, or `scope = "topic_agent"`
- **THEN** validation rejects the row with a deterministic diagnostic because project scope has no project actor or agent specialization

#### Scenario: Topic Workspace Manifest accepts topic params
- **WHEN** a Topic Workspace Manifest contains a `[[user_plugin_runtime_params]]` row
- **THEN** validation accepts the row only when `scope` is `research_topic`, `topic_actor`, or `topic_agent`, or when the scope is omitted and defaults to `research_topic`

#### Scenario: Topic Actor param requires actor name
- **WHEN** a runtime param row uses `scope = "topic_actor"`
- **THEN** validation requires `topic_actor_name` and applies the row only to an exact matching Effective Topic Actor Context

#### Scenario: Topic Agent param requires agent name
- **WHEN** a runtime param row uses `scope = "topic_agent"`
- **THEN** validation requires `topic_agent_name` and applies the row only to an exact matching Effective Agent Context Agent Name

#### Scenario: Param key is namespaced by plugin
- **WHEN** the system reports, gets, sets, unsets, or explains a runtime param
- **THEN** the effective param id is `<plugin_id>:<param-key>`
- **AND** the stored TOML row keeps `plugin_id` and `key` as separate fields

### Requirement: Runtime Param Value Contract
The system SHALL validate runtime param definitions and values before exposing them to callback skills or other plugin behavior.

#### Scenario: Supported value types are bounded
- **WHEN** a runtime param defines `value_type`
- **THEN** validation accepts only `string`, `bool`, `integer`, `number`, `enum`, and `string_list` in the initial version

#### Scenario: Enum value must be allowed
- **WHEN** a runtime param has `value_type = "enum"`
- **THEN** validation requires non-empty `allowed_values` and rejects any selected value that is not in that list

#### Scenario: Topic value can omit inherited definition metadata
- **WHEN** a Topic Workspace Manifest row supplies `plugin_id`, `key`, and `value` for a param already defined by a Project Manifest row or imported default
- **THEN** validation may use the inherited `value_type`, `allowed_values`, and description metadata to validate the topic value

#### Scenario: Topic value without broader definition must be self-defining
- **WHEN** a Topic Workspace Manifest row supplies `plugin_id`, `key`, and `value` for a param that has no applicable Project Manifest or project import definition
- **THEN** validation accepts the row only when it supplies complete definition metadata for the value type
- **AND** enum params must include non-empty `allowed_values`

#### Scenario: Conflicting metadata is rejected
- **WHEN** a more specific runtime param row supplies `value_type` or `allowed_values` that conflict with an applicable broader definition for the same param id
- **THEN** validation rejects the row with a deterministic diagnostic rather than treating it as a separate param definition

#### Scenario: Secret-like params are rejected
- **WHEN** a runtime param key, metadata field, import row, or value contains secret-like material such as a token, API key, password, credential, or private key
- **THEN** validation rejects the material without printing the secret-like value in diagnostics

### Requirement: Runtime Param Import Layers
The system SHALL support TOML param imports as default layers before explicit local runtime param rows.

#### Scenario: Project import contributes project defaults
- **WHEN** a Project Manifest declares `[[user_plugin_runtime_param_imports]]`
- **THEN** the referenced TOML file contributes only project-scope runtime param rows before Project Manifest explicit runtime param rows are applied
- **AND** relative import paths resolve from the directory containing the Project Manifest

#### Scenario: Topic import contributes topic defaults
- **WHEN** a Topic Workspace Manifest declares `[[user_plugin_runtime_param_imports]]`
- **THEN** the referenced TOML file contributes only `research_topic`, `topic_actor`, and `topic_agent` runtime param rows before Topic Workspace Manifest explicit runtime param rows are applied
- **AND** relative import paths resolve from the directory containing the Topic Workspace Manifest

#### Scenario: Absolute import path is rejected
- **WHEN** a runtime param import row uses an absolute path
- **THEN** validation rejects the import with a deterministic diagnostic in the initial implementation

#### Scenario: Local explicit value overrides imported value
- **WHEN** an imported runtime param and an explicit manifest runtime param have the same param id and applicable scope selector
- **THEN** the explicit manifest row overrides the imported value in the effective resolution result

#### Scenario: Imports are param-only
- **WHEN** an import TOML file contains User Plugin registrations, callback declarations, callback sources, nested imports, or unsupported top-level tables
- **THEN** validation rejects or ignores the unsupported material with deterministic diagnostics and does not install callbacks or register plugins from the import file

#### Scenario: Import explain names source file
- **WHEN** `user-plugin-params explain` reports a candidate value from an import
- **THEN** the output includes the import declaration source, imported file path, imported row scope, selected value, and whether the value was overridden

### Requirement: Runtime Param Resolution Order
The system SHALL resolve effective runtime param values with the layer order project-scope imports, project-scope explicit params, topic-scope imports, and topic-scope explicit params.

#### Scenario: Project explicit overrides project import
- **WHEN** a project import and Project Manifest explicit row both define the same param id
- **THEN** the Project Manifest explicit row wins before any topic-scope layers are considered

#### Scenario: Topic import overrides project explicit
- **WHEN** a Project Manifest explicit row and Topic Workspace Manifest import both define the same param id for the selected effective context
- **THEN** the topic-scope imported row wins

#### Scenario: Topic explicit overrides topic import
- **WHEN** a Topic Workspace Manifest import and Topic Workspace Manifest explicit row both define the same param id for the selected effective context
- **THEN** the Topic Workspace Manifest explicit row wins

#### Scenario: Research Topic value applies to topic workers
- **WHEN** a user gets a param for a selected Research Topic with a Topic Actor or Topic Agent selector and no exact worker-specific row overrides it
- **THEN** the applicable `scope = "research_topic"` topic value is used

#### Scenario: Topic Actor and Topic Agent selectors are exclusive
- **WHEN** a user requests an effective runtime param value with both Topic Actor and Topic Agent selectors
- **THEN** the command rejects the request with a deterministic diagnostic

#### Scenario: Topic Agent CLI selector is canonical
- **WHEN** a user selects a topic-agent-scoped User Plugin or runtime param value through a new plugin command
- **THEN** the documented canonical CLI selector is `--topic-agent`
- **AND** any accepted `--agent` spelling is treated as a compatibility alias for the same Effective Agent Context Agent Name

### Requirement: Runtime Param CLI Surface
The system SHALL expose a generic `isomer-cli project user-plugin-params` command group for runtime param definition, mutation, lookup, explanation, import management, and validation.

#### Scenario: Get command is read-only
- **WHEN** a user runs `isomer-cli --print-json project user-plugin-params get <param-id>` with optional topic, Topic Actor, or Topic Agent selectors
- **THEN** the command returns the effective value, value type, plugin id, param key, effective scope, source metadata, and diagnostics without mutating manifests or import files

#### Scenario: Set command writes selected layer
- **WHEN** a user runs `isomer-cli project user-plugin-params set <param-id> --value <value>` with Project or topic selectors
- **THEN** the command writes or updates only the selected manifest layer and reports the previous value, new value, selected scope, and source file

#### Scenario: Unset command removes selected layer only
- **WHEN** a user runs `isomer-cli project user-plugin-params unset <param-id>` with Project or topic selectors
- **THEN** the command removes or inactivates only the matching explicit row in the selected layer and leaves imported defaults and broader scope values intact

#### Scenario: Import add writes selected layer
- **WHEN** a user runs `isomer-cli project user-plugin-params import add --plugin-id <plugin-id> --path <path>` with Project or topic selectors
- **THEN** the command writes an import row to the selected manifest layer after validating the import file and reports the import id, path, scope, and diagnostics

#### Scenario: Validate checks reachable material
- **WHEN** a user runs `isomer-cli project user-plugin-params validate` with optional topic selectors
- **THEN** the command validates applicable User Plugin registrations, runtime param rows, import rows, imported files, type constraints, scope selectors, duplicate active explicit rows, and secret-like material

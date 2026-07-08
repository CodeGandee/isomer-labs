# toolbox-runtime-configuration Specification

## Purpose
Define Toolbox registration and runtime-param configuration across Project Manifest and Topic Workspace Manifest layers.

## Requirements
### Requirement: Toolbox Registration CRUD
The system SHALL expose Toolbox registrations as project CLI resources that can be installed, listed, shown, explained, enabled, disabled, source-updated, uninstalled, and validated without editing packaged system skill assets.

#### Scenario: Toolbox install records project registration
- **WHEN** a user runs `isomer-cli project toolboxes install --toolbox-dir <path>` without a Research Topic selector
- **THEN** the system validates the Toolbox manifest, writes or updates a Project Manifest `[[toolboxes]]` row with `scope = "project"`, and reports the Toolbox id, source path, status, scope, and diagnostics

#### Scenario: Toolbox install derives id from manifest
- **WHEN** a user runs `isomer-cli project toolboxes install --toolbox-dir <path>`
- **THEN** the command reads `toolbox_id` from the Toolbox manifest
- **AND** the command does not take a positional Toolbox id argument

#### Scenario: Callback install records Toolbox registration
- **WHEN** a user runs `isomer-cli project skill-callbacks install --toolbox-dir <path>` with Project or topic selectors
- **THEN** the system ensures a matching `[[toolboxes]]` registration exists at the same selected scope
- **AND** it preserves runtime params, imports, callback records for other Toolboxes, and Toolbox registrations for other scopes

#### Scenario: Toolbox install records topic registration
- **WHEN** a user runs `isomer-cli project toolboxes install --toolbox-dir <path> --topic <topic-id>`
- **THEN** the system validates the Toolbox manifest, writes or updates a Topic Workspace Manifest `[[toolboxes]]` row with `scope = "research_topic"`, and reports the Toolbox id, source path, status, scope, selected Research Topic, and diagnostics

#### Scenario: Toolbox enablement is scope-specific
- **WHEN** a user enables or disables a Toolbox with Project, Research Topic, Topic Actor, or Topic Agent selectors
- **THEN** the system writes only the selected scope layer and does not delete broader or narrower Toolbox registrations

#### Scenario: Toolbox uninstall removes selected layer only
- **WHEN** a user uninstalls a Toolbox with a selected scope
- **THEN** the system removes or archives only that scope's `[[toolboxes]]` row and leaves callback records, runtime params, imports, and other scope registrations untouched

### Requirement: Toolbox Runtime Param Table Schema
The system SHALL represent Toolbox-specific runtime params with `[[toolbox_runtime_params]]` tables that use the same authoring shape in Project Manifests, Topic Workspace Manifests, and param import files.

#### Scenario: Project Manifest accepts project params
- **WHEN** the Project Manifest contains a `[[toolbox_runtime_params]]` row
- **THEN** validation accepts the row only when `scope = "project"` or the scope is omitted and defaults to `project`

#### Scenario: Topic Workspace Manifest accepts topic params
- **WHEN** a Topic Workspace Manifest contains a `[[toolbox_runtime_params]]` row
- **THEN** validation accepts the row only when `scope` is `research_topic`, `topic_actor`, or `topic_agent`, or when the scope is omitted and defaults to `research_topic`

#### Scenario: Topic Actor param requires actor name
- **WHEN** a runtime param row uses `scope = "topic_actor"`
- **THEN** validation requires `topic_actor_name` and applies the row only to an exact matching Effective Topic Actor Context

#### Scenario: Topic Agent param requires agent name
- **WHEN** a runtime param row uses `scope = "topic_agent"`
- **THEN** validation requires `topic_agent_name` and applies the row only to an exact matching Effective Agent Context Agent Name

#### Scenario: Param key is namespaced by Toolbox
- **WHEN** the system reports, gets, sets, unsets, or explains a runtime param
- **THEN** the effective param id is `<toolbox_id>:<param-key>`
- **AND** the stored TOML row keeps `toolbox_id` and `key` as separate fields

### Requirement: Toolbox Runtime Param Import Layers
The system SHALL support TOML param imports as default layers before explicit local runtime param rows.

#### Scenario: Project import contributes project defaults
- **WHEN** a Project Manifest declares `[[toolbox_runtime_param_imports]]`
- **THEN** the referenced TOML file contributes only project-scope runtime param rows before Project Manifest explicit runtime param rows are applied
- **AND** relative import paths resolve from the directory containing the Project Manifest

#### Scenario: Topic import contributes topic defaults
- **WHEN** a Topic Workspace Manifest declares `[[toolbox_runtime_param_imports]]`
- **THEN** the referenced TOML file contributes only `research_topic`, `topic_actor`, and `topic_agent` runtime param rows before Topic Workspace Manifest explicit runtime param rows are applied
- **AND** relative import paths resolve from the directory containing the Topic Workspace Manifest

#### Scenario: Imports are param-only
- **WHEN** an import TOML file contains Toolbox registrations, callback declarations, callback sources, nested imports, or unsupported top-level tables
- **THEN** validation rejects the unsupported material with deterministic diagnostics and does not install callbacks or register Toolboxes from the import file

#### Scenario: Old runtime param schema is rejected
- **WHEN** validation reads an import TOML file with an old runtime param schema version, old table name, or old identity field
- **THEN** validation rejects the import with a deterministic diagnostic

### Requirement: Toolbox Runtime Param Resolution Order
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

#### Scenario: Topic Agent CLI selector is canonical
- **WHEN** a user selects a topic-agent-scoped Toolbox or runtime param value through a Toolbox command
- **THEN** the documented canonical CLI selector is `--topic-agent`

### Requirement: Toolbox Runtime Param CLI Surface
The system SHALL expose `isomer-cli project toolbox-params` for runtime param definition, mutation, lookup, explanation, import management, and validation.

#### Scenario: Get command is read-only
- **WHEN** a user runs `isomer-cli --print-json project toolbox-params get <param-id>` with optional topic, Topic Actor, or Topic Agent selectors
- **THEN** the command returns the effective value, value type, Toolbox id, param key, effective scope, source metadata, and diagnostics without mutating manifests or import files

#### Scenario: Set command writes selected layer
- **WHEN** a user runs `isomer-cli project toolbox-params set <param-id> --value <value>` with Project or topic selectors
- **THEN** the command writes or updates only the selected manifest layer and reports the previous value, new value, selected scope, and source file

#### Scenario: Import add writes selected layer
- **WHEN** a user runs `isomer-cli project toolbox-params import add <toolbox-id> <path>` with Project or topic selectors
- **THEN** the command writes an import row to the selected manifest layer after validating the import file and reports the import id, path, scope, and diagnostics

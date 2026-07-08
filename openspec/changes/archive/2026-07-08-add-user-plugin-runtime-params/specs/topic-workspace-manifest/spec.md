## ADDED Requirements

### Requirement: Topic User Plugin Configuration Tables
The Topic Workspace Manifest SHALL support topic-scope User Plugin registrations, runtime param imports, and runtime params using the same table shapes as the Project Manifest.

#### Scenario: Topic manifest meaning includes plugin configuration
- **WHEN** documentation or validation describes the Topic Workspace Manifest
- **THEN** it treats topic-scope User Plugin registrations, runtime param imports, and runtime params as topic-owned configuration in addition to topology and path configuration
- **AND** it does not treat those rows as Project Config Directory state, Project Manifest overrides, or Workspace Runtime state

#### Scenario: Topic manifest stores plugin registration
- **WHEN** the Topic Workspace Manifest contains a `[[user_plugins]]` row
- **THEN** validation accepts the row only when its scope is `research_topic`, `topic_actor`, or `topic_agent`, or when the scope is omitted and defaults to `research_topic`

#### Scenario: Topic manifest stores param imports
- **WHEN** the Topic Workspace Manifest contains a `[[user_plugin_runtime_param_imports]]` row
- **THEN** validation accepts the row only for topic-scope layers and resolves relative import paths from the directory containing the Topic Workspace Manifest

#### Scenario: Topic manifest stores runtime params
- **WHEN** the Topic Workspace Manifest contains a `[[user_plugin_runtime_params]]` row
- **THEN** validation accepts the row only for `research_topic`, `topic_actor`, or `topic_agent` scope and rejects project-scope runtime params in the topic-owned manifest

#### Scenario: Topic Actor selector refers to manifest actor bindings
- **WHEN** a User Plugin registration or runtime param row uses `scope = "topic_actor"`
- **THEN** validation requires `topic_actor_name` and verifies it against the selected Topic Workspace Manifest actor bindings when those bindings are available

#### Scenario: Topic Agent selector is topic-local
- **WHEN** a User Plugin registration or runtime param row uses `scope = "topic_agent"`
- **THEN** validation requires `topic_agent_name` and treats it as a topic-local Agent Name selector for Effective Agent Context rather than as a Project-level worker identity

#### Scenario: Existing path bindings remain independent
- **WHEN** the Topic Workspace Manifest contains User Plugin configuration tables and semantic path binding tables
- **THEN** Workspace Path Resolution continues to use semantic path binding tables and does not treat User Plugin runtime params as semantic workspace surface labels

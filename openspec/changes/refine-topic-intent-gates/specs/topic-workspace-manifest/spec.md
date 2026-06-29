## ADDED Requirements

### Requirement: Intent Storage Profiles and Default Bindings
The Topic Workspace Manifest and built-in default layout profile SHALL support reserved topic intent and env target-spec semantic labels through accepted storage profiles.

#### Scenario: Default profile declares intent storage profiles
- **WHEN** the built-in `isomer-default.v1` layout profile is used for a Topic Workspace
- **THEN** `topic.intent.overview`, `topic.intent.topic_env_requirements`, and `topic.intent.agent_env_requirements` use the `topic_intent_source_file` storage profile
- **AND** `topic.env.topic_setup_target_spec` and `topic.env.agent_setup_target_spec` use the `topic_env_target_spec_file` storage profile

#### Scenario: Source intent storage profile is user-editable
- **WHEN** a binding uses the `topic_intent_source_file` storage profile
- **THEN** validation treats the surface as topic-scoped, durable, user-editable, Markdown-compatible, file-kind material
- **AND** validation does not classify the surface as runtime-internal, cache-like, disposable, or service-only output

#### Scenario: Target spec storage profile is service-owned but reviewable
- **WHEN** a binding uses the `topic_env_target_spec_file` storage profile
- **THEN** validation treats the surface as topic-scoped, durable, reviewable, Markdown-compatible, file-kind material used as a setup service target spec
- **AND** validation does not classify the surface as user source intent, runtime-internal state, cache-like material, or a disposable execution log

### Requirement: Intent Semantic Binding Overrides
The Topic Workspace Manifest SHALL allow safe overrides of accepted reserved intent and target-spec labels without allowing skills to bypass semantic path resolution.

#### Scenario: Manifest override for intent label is accepted
- **WHEN** a Topic Workspace Manifest declares `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.agent_env_requirements`, `topic.env.topic_setup_target_spec`, or `topic.env.agent_setup_target_spec` with a path and the expected storage profile
- **THEN** manifest validation accepts the binding when the resolved path is safe for the selected Topic Workspace and matches the label scope and path kind

#### Scenario: Wrong storage profile is rejected
- **WHEN** a manifest binding for a reserved intent or target-spec label uses an unknown storage profile or a storage profile that does not match the label
- **THEN** manifest validation reports the binding as invalid before Workspace Path Resolution exposes it as usable

#### Scenario: Unsafe intent override is rejected
- **WHEN** a manifest binding for an intent or target-spec label resolves outside the Project root, inside `.isomer-labs/`, into another registered Topic Workspace, or into an Agent Workspace-private surface
- **THEN** manifest validation rejects the binding for dependent commands

#### Scenario: CLI registration can bind intent labels
- **WHEN** a user runs a supported path registration command for one of the reserved intent or target-spec labels with a path and expected storage profile
- **THEN** the command validates the same namespace, storage profile, duplicate binding, and path safety rules as manifest loading before writing the binding

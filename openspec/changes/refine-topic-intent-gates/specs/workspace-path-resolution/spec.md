## ADDED Requirements

### Requirement: Topic Intent Semantic Path Labels
Workspace Path Resolution SHALL expose built-in topic-scoped semantic labels for topic intent source surfaces and env setup target specs.

#### Scenario: Intent labels are in the effective catalog
- **WHEN** a command queries the effective semantic surface catalog for a Topic Workspace
- **THEN** the catalog includes `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.agent_env_requirements`, `topic.env.topic_setup_target_spec`, and `topic.env.agent_setup_target_spec`
- **AND** each entry includes the semantic label, storage profile, path kind, scope, owner, durability, source, source detail, and diagnostics when available

#### Scenario: Default layout resolves intent labels
- **WHEN** a Topic Workspace uses the built-in `isomer-default.v1` layout profile and no higher-precedence binding overrides an intent label
- **THEN** Workspace Path Resolution resolves `topic.intent.overview` to `<topic-workspace>/intent/src/topic-overview.md`
- **AND** it resolves `topic.intent.topic_env_requirements` to `<topic-workspace>/intent/src/topic-env-gate.md`
- **AND** it resolves `topic.intent.agent_env_requirements` to `<topic-workspace>/intent/src/agent-env-gate.md`
- **AND** it resolves `topic.env.topic_setup_target_spec` to `<topic-workspace>/intent/derived/isomer-env-gate.md`
- **AND** it resolves `topic.env.agent_setup_target_spec` to `<topic-workspace>/intent/derived/isomer-agent-env-gate.md`

#### Scenario: Skills query labels before file access
- **WHEN** a skill needs to read, write, materialize, validate, or report a topic intent source surface or env setup target spec
- **THEN** it resolves the relevant semantic label through Workspace Path Resolution before touching a filesystem path
- **AND** it reports the semantic label and resolved path in outputs that mention the surface

#### Scenario: Intent label diagnostics block guessed paths
- **WHEN** Workspace Path Resolution cannot resolve an intent or target-spec label for the selected Topic Workspace
- **THEN** dependent skills report the resolver diagnostic instead of guessing an `intent/src`, `intent/derived`, `topic-def`, or `user-intent` path

### Requirement: Topic Intent Semantic Path Materialization
Workspace Path Resolution SHALL materialize topic intent and target-spec file surfaces through their resolved semantic labels without treating default layout paths as skill-owned constants.

#### Scenario: Source intent file materialization prepares parent directory
- **WHEN** a workflow materializes `topic.intent.overview`, `topic.intent.topic_env_requirements`, or `topic.intent.agent_env_requirements`
- **THEN** materialization creates or validates the parent directory for the resolved file path according to the selected storage profile
- **AND** it does not create placeholder source intent content unless the calling workflow owns the content write

#### Scenario: Target spec materialization prepares parent directory
- **WHEN** a workflow materializes `topic.env.topic_setup_target_spec` or `topic.env.agent_setup_target_spec`
- **THEN** materialization creates or validates the parent directory for the resolved target-spec file path according to the selected storage profile
- **AND** it leaves target-spec file content to the service skill that derives or accepts the operational spec

#### Scenario: Materialization output is label-based
- **WHEN** materialization completes, blocks, or reports an already-existing surface
- **THEN** the output includes the semantic label, resolved path, storage profile, source, source detail, and any blocker diagnostics

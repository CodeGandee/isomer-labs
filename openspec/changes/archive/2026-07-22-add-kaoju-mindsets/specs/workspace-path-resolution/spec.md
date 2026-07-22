## ADDED Requirements

### Requirement: Kaoju Mindset Derived Intent Has a Semantic Root
Workspace Path Resolution SHALL expose topic-scoped semantic directory label `topic.intent.kaoju_mindsets` for owner-editable Kaoju Mindset Source files derived from topic intent.

#### Scenario: Mindset root is in the effective catalog
- **WHEN** a caller lists semantic paths for a selected Topic Workspace
- **THEN** the effective catalog includes `topic.intent.kaoju_mindsets` with topic scope, directory path kind, owner-editable durable-directory traits, source, source detail, and diagnostics
- **AND** it describes the surface as derived intent rather than an Artifact record root, runtime directory, or disposable exchange surface

#### Scenario: Default mindset root is resolved
- **WHEN** a Topic Workspace uses `isomer-default.v1` and no higher-precedence binding overrides the label
- **THEN** `topic.intent.kaoju_mindsets` resolves to `<topic-workspace>/intent/derived/mindsets`
- **AND** no individual mindset key is embedded in the semantic root binding

#### Scenario: Mindset root is materialized
- **WHEN** the Kaoju topic-creation owner is authorized to derive or repair Mindset Sources
- **THEN** Workspace Path Resolution creates or validates the resolved directory according to its storage profile
- **AND** path materialization does not create placeholder JSON or infer which Source keys are required

#### Scenario: Skills resolve the root before file access
- **WHEN** a Kaoju skill needs to generate, copy, inspect, validate, edit, select, or report a Mindset Source
- **THEN** it resolves `topic.intent.kaoju_mindsets` for the selected Research Topic before filesystem access and reports the semantic label and resolved path when mentioning the surface
- **AND** resolver failure blocks the operation instead of guessing `intent/derived/mindsets`, using cwd, scanning sibling topics, or substituting a package resource at runtime

### Requirement: Mindset Source Children Are Deterministic and Path-Safe
Consumers of `topic.intent.kaoju_mindsets` SHALL map each validated `mindset_key` to exactly one safe child filename `<mindset_key>.json` beneath the resolved root.

#### Scenario: Valid key resolves a child
- **WHEN** a key matches `^[a-z0-9]+(?:[.-][a-z0-9]+)*$`
- **THEN** the consumer appends `.json` and confirms the normalized child remains directly beneath the root
- **AND** the JSON body's `mindset_key` must equal the filename key

#### Scenario: Unsafe child is requested
- **WHEN** a key or requested Source path is absolute, empty, contains a separator or traversal, has ambiguous normalization, omits `.json`, or resolves outside the root
- **THEN** path validation rejects it before read or write
- **AND** the consumer does not search for an alternative file

## ADDED Requirements

### Requirement: Kaoju Writing-Template Exchange Has a Semantic Path Surface
Workspace Path Resolution SHALL expose a built-in topic-scoped root for non-canonical named Kaoju template working copies.

#### Scenario: Exchange root is in the effective catalog
- **WHEN** a caller lists semantic paths for a selected Topic Workspace
- **THEN** the effective catalog includes `topic.paper.template_exchange_root` with topic scope, owner-editable durable-directory traits, source, source detail, storage profile, and diagnostics
- **AND** the surface is described as non-canonical exchange material rather than an Artifact record root

#### Scenario: Default exchange root is resolved
- **WHEN** the Topic Workspace uses the built-in default layout and no higher-precedence binding overrides the exchange root
- **THEN** `topic.paper.template_exchange_root` resolves to `<topic-workspace>/intent/derived/writing-template`
- **AND** a validated template name is appended by the Kaoju paper service rather than embedded in the root binding

#### Scenario: Main working directory is derived
- **WHEN** an unnamed export selects canonical `main` or underspecified update discovery reaches the topic-directory fallback
- **THEN** the Kaoju service or agent resolves the exchange root and selects child directory `main`
- **AND** it reports both the semantic root label and concrete `<resolved-root>/main/` path

#### Scenario: Skills and services do not guess the path
- **WHEN** a Kaoju skill or CLI service needs to export, discover, inspect, reconcile, validate, or report a template working directory
- **THEN** it queries Workspace Path Resolution for `topic.paper.template_exchange_root` before filesystem access
- **AND** resolver failure blocks the operation instead of falling back to `exports/kaoju-paper`, a remembered `intent/derived` path, or cwd-relative construction

#### Scenario: Named child is path safe
- **WHEN** a template name is appended to the resolved exchange root
- **THEN** validation accepts exactly one normalized path-safe name segment and confirms that the resulting default path remains beneath the root
- **AND** absolute paths, traversal, separators, empty names, and ambiguous normalization are rejected

#### Scenario: Exchange root is materialized
- **WHEN** an authorized template export materializes the effective exchange root
- **THEN** Workspace Path Resolution creates or validates the resolved directory according to its storage profile before the service creates the named child
- **AND** path materialization does not create canonical template content or an empty canonical record

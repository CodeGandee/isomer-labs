## MODIFIED Requirements

### Requirement: Kaoju Writing-Template Exchange Has a Semantic Path Surface
Workspace Path Resolution SHALL expose a built-in topic-scoped root for non-canonical named Kaoju template working copies at the plural default directory while preserving explicit compatibility bindings.

#### Scenario: Exchange root is in the effective catalog
- **WHEN** a caller lists semantic paths for a selected Topic Workspace
- **THEN** the effective catalog includes `topic.paper.template_exchange_root` with topic scope, owner-editable durable-directory traits, source, source detail, storage profile, and diagnostics
- **AND** the surface is described as non-canonical exchange material rather than an Artifact record root

#### Scenario: Default exchange root is resolved
- **WHEN** the Topic Workspace uses the built-in default layout and no higher-precedence binding overrides the exchange root
- **THEN** `topic.paper.template_exchange_root` resolves to `<topic-workspace>/intent/derived/writing-templates`
- **AND** the selected template kind and validated template name are appended by the Kaoju paper service rather than embedded in the root binding

#### Scenario: Main working directories are derived
- **WHEN** an unnamed export selects role-local `main` or underspecified update discovery reaches the topic-directory fallback
- **THEN** the Kaoju service or agent resolves the exchange root and selects `<resolved-root>/content/main/` or `<resolved-root>/latex/main/` for the already selected role
- **AND** it reports the semantic root label, role, name, and concrete path

#### Scenario: Skills and services do not guess the path
- **WHEN** a Kaoju skill or CLI service needs to export, discover, inspect, reconcile, validate, migrate, or report a template working directory
- **THEN** it queries Workspace Path Resolution for `topic.paper.template_exchange_root` before filesystem access
- **AND** resolver failure blocks the operation instead of falling back to `exports/kaoju-paper`, a remembered `intent/derived` path, or cwd-relative construction

#### Scenario: Named child is path safe
- **WHEN** a template kind and name are appended to the resolved exchange root
- **THEN** validation accepts a registered role directory and exactly one normalized path-safe name segment and confirms that the resulting default path remains beneath the root
- **AND** absolute paths, traversal, separators, empty names, unknown roles, and ambiguous normalization are rejected

#### Scenario: Exchange root is materialized
- **WHEN** an authorized template initialization or export materializes the effective exchange root
- **THEN** Workspace Path Resolution creates or validates the resolved directory according to its storage profile before the service creates role and name children
- **AND** path materialization alone does not create canonical template content or an empty canonical record

#### Scenario: Explicit singular binding remains authoritative
- **WHEN** a Topic Workspace Manifest or higher-precedence source explicitly binds `topic.paper.template_exchange_root` to `intent/derived/writing-template`
- **THEN** resolution preserves that binding and reports a legacy singular-path advisory
- **AND** the resolver does not rewrite the manifest, move files, or substitute the plural default

#### Scenario: Unbound legacy singular root is detected
- **WHEN** no higher-precedence binding exists and the selected Topic Workspace contains the exact legacy sibling `intent/derived/writing-template`
- **THEN** the effective path remains the plural default and compatibility diagnostics report the legacy root and migration posture
- **AND** detection does not scan arbitrary directories, merge content, or mutate either root

#### Scenario: Singular and plural roots conflict
- **WHEN** migration inspection finds non-equivalent content beneath both the legacy singular root and the plural root
- **THEN** migration reports the conflicting role and name paths and blocks apply
- **AND** both roots remain unchanged until an actor explicitly reconciles the content

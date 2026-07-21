## ADDED Requirements

### Requirement: Reusable Project Web Read Context
Project Web SHALL reuse one validated Project state for read requests while the relevant Project configuration revision remains unchanged.

#### Scenario: Concurrent startup reads share validation
- **WHEN** several Project Web API requests need Project state concurrently for the same configuration revision
- **THEN** the backend SHALL perform one full Project validation pass
- **AND** every request SHALL receive equivalent Project state and diagnostics

#### Scenario: Unchanged follow-up read uses cached state
- **WHEN** a later read request observes the same Project configuration revision
- **THEN** the backend SHALL reuse the validated state without reparsing callback registries or the packaged insertion-point catalog

#### Scenario: Project configuration changes
- **WHEN** the Project Manifest, a Research Topic Config, local context, or a referenced callback registry changes
- **THEN** the next state-dependent read SHALL invalidate the cached state and validate the new revision

#### Scenario: Runtime data changes
- **WHEN** Workspace Runtime records or query-index rows change without a Project configuration change
- **THEN** Project Web SHALL retain the validated Project state
- **AND** runtime, graph, and record queries SHALL still read current Workspace Runtime data

### Requirement: Bounded Project Web Startup
Project Web SHALL make the shell and requested viewer usable without waiting for unrelated data or traversing Topic Workspace environments.

#### Scenario: Shell loads before backend data
- **WHEN** a user opens Project Web while backend read queries are pending
- **THEN** the browser SHALL render the workbench shell and non-blocking loading states

#### Scenario: Deep-linked viewer opens independently
- **WHEN** the URL identifies a Research Topic and openable viewer
- **THEN** descriptor resolution and viewer loading SHALL begin without waiting for the Project Explorer response

#### Scenario: Reference Idea Graph meets acceptance budget
- **WHEN** Playwright opens the Idea Graph for `flash-attention-4-whitebox-runtime-model` on the local reference Project
- **THEN** the Explorer skeleton SHALL appear within two seconds after DOM content loads
- **AND** the first graph summary SHALL appear within five seconds under normal local development load

#### Scenario: Startup ignores enclosed environments
- **WHEN** the selected Topic Workspace contains a large `.pixi` environment
- **THEN** Project Web startup SHALL NOT traverse, enumerate, or transfer that environment

# project-web-gui Specification

## Purpose
TBD - created by archiving change add-project-web-gui. Update Purpose after archive.
## Requirements
### Requirement: Local Project Web Service
The system SHALL provide a local single-user web service that targets one selected Isomer Project root per process.

#### Scenario: Serve selected Project
- **WHEN** a user starts the web service with an explicit Project root
- **THEN** the service resolves that root as an Isomer Project and exposes the resolved Project summary through an HTTP API

#### Scenario: Invalid Project reports diagnostics
- **WHEN** the selected path is not a valid Isomer Project
- **THEN** the service reports deterministic Project discovery diagnostics instead of silently initializing or mutating the path

#### Scenario: Default bind is local
- **WHEN** the service starts without a host override
- **THEN** it binds to a loopback host suitable for single-user local browsing

### Requirement: Project and Topic Read APIs
The web service SHALL expose read APIs for Project, Research Topic, Topic Workspace, Topic Actor, and Workspace Runtime summaries.

#### Scenario: List Research Topics
- **WHEN** the frontend requests the Project topics
- **THEN** the API returns registered Research Topics with status, config path, Topic Workspace id, and resolved Topic Workspace path when available

#### Scenario: Show Topic Workspace state
- **WHEN** the frontend requests one Research Topic
- **THEN** the API returns selected Effective Topic Context data, Topic Workspace path, Topic Workspace Manifest summary, Topic Actors, and diagnostics

#### Scenario: Show runtime summary
- **WHEN** the frontend requests Workspace Runtime state for one Research Topic
- **THEN** the API returns runtime metadata, counts, latest readiness when available, path plans, and diagnostics without mutating runtime state

### Requirement: Research Record Browser APIs
The web service SHALL expose topic-scoped APIs for browsing indexed research records and canonical record details.

#### Scenario: List indexed records
- **WHEN** the frontend requests records for a Research Topic with optional filters
- **THEN** the API returns query-index record summaries using read-only Workspace Runtime access

#### Scenario: Export dashboard view
- **WHEN** the frontend requests a named export view such as `timeline`, `graph`, `dashboard`, `ideas`, `experiments`, or `claims`
- **THEN** the API returns query-index nodes, edges, files, ideas, routes, metrics, claims, facts, and diagnostics for that Topic Workspace

#### Scenario: Show record detail
- **WHEN** the frontend opens one record
- **THEN** the API returns lifecycle metadata and structured payload metadata and can include canonical payload JSON on request

#### Scenario: Render record Markdown
- **WHEN** the frontend requests rendered Markdown for a structured record
- **THEN** the API renders from the managed payload JSON and resolved Jinja2 template without writing a generated Markdown file

#### Scenario: Show record lineage and files
- **WHEN** the frontend requests lineage, files, or facets for one record
- **THEN** the API returns query-index derived data without repairing missing index rows

### Requirement: Explicit Query-index Maintenance
The web service SHALL keep query-index maintenance as explicit user-triggered actions.

#### Scenario: Validate index
- **WHEN** the frontend requests index validation for a Research Topic
- **THEN** the API returns stale, missing, or inconsistent query-index diagnostics without mutation

#### Scenario: Rebuild index
- **WHEN** the frontend sends an explicit rebuild request for a Research Topic or selected record id
- **THEN** the API refreshes derived query-index rows from canonical runtime records and payload files

#### Scenario: Cleanup index
- **WHEN** the frontend sends an explicit cleanup request with selectors and apply mode
- **THEN** the API previews or applies cleanup only to derived query-index rows according to existing query-index rules

### Requirement: Packaged TypeScript Frontend
The system SHALL provide a TypeScript-authored frontend that is served by the local web service.

#### Scenario: Serve frontend shell
- **WHEN** a user opens the service root URL
- **THEN** the service returns the packaged frontend shell

#### Scenario: Browse Project interactively
- **WHEN** the frontend loads successfully
- **THEN** it can display Project status, topic list, topic overview, record table, export views, and record details using the web APIs

#### Scenario: Static assets are local
- **WHEN** the frontend loads assets
- **THEN** it uses files served by the local web service rather than a required external frontend service


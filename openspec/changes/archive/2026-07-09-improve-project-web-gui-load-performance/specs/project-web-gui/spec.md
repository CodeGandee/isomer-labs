## MODIFIED Requirements

### Requirement: Local Project Web Service
The system SHALL provide a local single-user web service that targets one selected Isomer Project root per process and supports explicit normal and debug launch cache modes.

#### Scenario: Serve selected Project
- **WHEN** a user starts the web service with an explicit Project root
- **THEN** the service resolves that root as an Isomer Project and exposes the resolved Project summary through an HTTP API

#### Scenario: Invalid Project reports diagnostics
- **WHEN** the selected path is not a valid Isomer Project
- **THEN** the service reports deterministic Project discovery diagnostics instead of silently initializing or mutating the path

#### Scenario: Default bind is local
- **WHEN** the service starts without a host override
- **THEN** it binds to a loopback host suitable for single-user local browsing

#### Scenario: Normal launch uses production cache behavior
- **WHEN** the service starts without a debug cache-mode override
- **THEN** it serves the GUI in normal launch mode with compressed eligible responses, immutable cache headers for content-hashed static assets, and a fresh HTML shell that can discover the latest asset URLs

#### Scenario: Debug launch prevents browser cache interference
- **WHEN** the service starts in debug launch mode
- **THEN** it applies no-store cache behavior to the GUI shell, static assets, and API responses so browser cache cannot hide frontend or backend changes during debugging

#### Scenario: Launch mode is visible
- **WHEN** the service starts in normal or debug launch mode
- **THEN** the selected cache mode is visible through CLI help, startup diagnostics, or a read-only service diagnostics response

### Requirement: Research Record Browser APIs
The web service SHALL expose topic-scoped APIs for browsing indexed research records and canonical record details, with list endpoints returning lightweight view projections by default.

#### Scenario: List indexed records
- **WHEN** the frontend requests records for a Research Topic with optional filters
- **THEN** the API returns query-index record summaries using read-only Workspace Runtime access
- **AND** the default response includes the fields needed for browsing, filtering, sorting, row colorization, and opening details without embedding full payload metadata or canonical JSON for every record

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

#### Scenario: List response honors record count controls
- **WHEN** the frontend requests a bounded number of records for a table view
- **THEN** the API returns at most that requested count plus diagnostics needed to explain truncation, partial index state, or unsupported filters

### Requirement: Packaged TypeScript Frontend
The system SHALL provide a TypeScript-authored frontend that is served by the local web service with cache-mode-aware static asset behavior.

#### Scenario: Serve frontend shell
- **WHEN** a user opens the service root URL
- **THEN** the service returns the packaged frontend shell

#### Scenario: Browse Project interactively
- **WHEN** the frontend loads successfully
- **THEN** it can display Project status, topic list, topic overview, record table, export views, and record details using the web APIs

#### Scenario: Static assets are local
- **WHEN** the frontend loads assets
- **THEN** it uses files served by the local web service rather than a required external frontend service

#### Scenario: Normal launch reuses unchanged assets
- **WHEN** the frontend is served in normal launch mode
- **THEN** JavaScript and CSS asset URLs include content-derived cache keys or hashes
- **AND** the service marks those hashed assets cacheable across browser sessions until their URL changes

#### Scenario: Debug launch reloads changed assets
- **WHEN** the frontend is served in debug launch mode
- **THEN** the browser receives no-store headers for frontend assets and API responses so a refresh fetches current local files

#### Scenario: Eligible frontend responses are compressed
- **WHEN** a browser requests JavaScript, CSS, HTML, or JSON and advertises supported content encoding
- **THEN** the service returns compressed content for eligible responses above the configured size threshold

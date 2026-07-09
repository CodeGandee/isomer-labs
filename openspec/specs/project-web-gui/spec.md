# project-web-gui Specification

## Purpose
TBD - created by archiving change add-project-web-gui. Update Purpose after archive.
## Requirements
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

### Requirement: Project Web Uses Documented Data Contracts
The Project Web backend and frontend SHALL treat documented UI contracts as the handoff surface for GUI-renderable topic data.

#### Scenario: Backend returns contract-compatible payloads
- **WHEN** a Project Web API returns a payload consumed directly by a GUI panel
- **THEN** the payload SHALL satisfy the required fields of the corresponding UI contract
- **AND** the payload MAY include additional fields for diagnostics, future viewers, or JSON inspection

#### Scenario: Frontend receives extra fields
- **WHEN** the TypeScript GUI receives a contract-compatible payload with extra fields
- **THEN** the GUI SHALL render from the documented required and optional fields it knows about
- **AND** it SHALL NOT fail solely because the payload contains additional fields

#### Scenario: Frontend receives missing required fields
- **WHEN** the TypeScript GUI or backend validation detects a payload missing required UI contract fields
- **THEN** the system SHALL report a diagnostic, validation error, or safe empty state instead of crashing the workbench

#### Scenario: Contract docs guide new views
- **WHEN** a new Project Web topic panel or viewer is added
- **THEN** the implementation SHALL add or update a `docs/ui/contracts/` page and schema coverage for the GUI-facing payload shape before relying on the new contract in the frontend

### Requirement: Graphs Navigation Is Idea-led
Project Web SHALL make the visible Research Topic `Graphs` navigation focus on Research Idea progress views.

#### Scenario: Graphs exposes idea views
- **WHEN** a user expands a Research Topic in the Project Explorer
- **THEN** the `Graphs` section shows openable views for Idea Graph and Idea Timeline
- **AND** both views target the selected Research Topic

#### Scenario: Dense non-idea graph sections are hidden
- **WHEN** a user expands the `Graphs` section
- **THEN** Project Web does not show `Artifact Overview`, `Experiment Records`, or `Paper Revisions` as visible graph entries

#### Scenario: Removed dense graph URLs do not restore views
- **WHEN** a user opens an old Project Web URL for `artifact-overview`, `experiment-records`, or `paper-revisions`
- **THEN** Project Web does not render the removed dense graph view
- **AND** it reports or routes through unsupported graph-scope behavior

#### Scenario: Idea graph opens relationship view
- **WHEN** a user opens the Idea Graph view
- **THEN** Project Web opens the existing idea relationship graph backed by the `idea-lineage` read model

#### Scenario: Idea timeline opens table view
- **WHEN** a user opens the Idea Timeline view
- **THEN** Project Web opens a table-oriented view of Research Ideas for the same selected Research Topic

### Requirement: Graph View History Uses Idea View Identity
Project Web SHALL keep browser history and workbench openable identity stable for separate Idea Graph and Idea Timeline views.

#### Scenario: Idea graph URL is stable
- **WHEN** a user opens the Idea Graph view for a Research Topic
- **THEN** browser history records a stable graph/view state that can restore that idea relationship view

#### Scenario: Idea timeline URL is stable
- **WHEN** a user opens the Idea Timeline view for a Research Topic
- **THEN** browser history records a stable graph/view state that can restore that timeline table view

### Requirement: Idea Timeline Unified Fuzzy Search
The Idea Timeline view SHALL expose a single fuzzy text search bar for table entries, matching the Idea Graph search usage pattern.

#### Scenario: Search matches any table field
- **WHEN** the user types text into the Idea Timeline search bar
- **THEN** the timeline evaluates the query against display key, title, aliases, one-liner, family, status, idea id, parent display-key labels, parent titles, relation kinds, and other rendered table-entry fields
- **AND** matching is fuzzy enough to tolerate partial terms and normal text casing differences

#### Scenario: Search reaches supporting rows without changing visibility
- **WHEN** the search query matches a supporting Research Idea row
- **AND** the Supporting Records flag is off
- **THEN** the supporting row remains hidden
- **AND** enabling Supporting Records reveals matching supporting rows without changing the search text

#### Scenario: Timeline removes field-specific search controls
- **WHEN** the user opens Idea Timeline
- **THEN** the view presents one search bar instead of separate status, relation, or field-specific text inputs

### Requirement: Idea Timeline Display Key Labels
The Project Web GUI SHALL render Research Idea display keys in the `I-<index>` format wherever the Idea Timeline shows short idea identity.

#### Scenario: Timeline row shows hyphenated key
- **WHEN** a timeline row has `display_key: "I-7"`
- **THEN** the visible key column renders `I-7`
- **AND** the row identity remains keyed by canonical `idea_id`, not by row position

#### Scenario: Parent labels use hyphenated keys
- **WHEN** a timeline row renders parent references
- **THEN** parent references use parent `display_key` values such as `I-2` when available
- **AND** fall back to canonical parent `idea_id` only when the display key is missing

### Requirement: Idea Timeline Colorization Defaults Off
The Idea Timeline view SHALL render with row category colorization disabled by default while preserving opt-in row color support.

#### Scenario: Default table has no category background colors
- **WHEN** the user opens Idea Timeline with no stored row-color preference
- **THEN** primary and supporting rows do not use category background colors
- **AND** the table still exposes non-color cues for selection and row metadata

#### Scenario: User enables row colorization
- **WHEN** the user enables Idea Timeline row coloring in Project Settings
- **THEN** the timeline applies configured primary and supporting row colors to matching visible rows


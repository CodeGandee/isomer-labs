# isomer-op-gui-mgr-skill Specification

## Purpose
TBD - created by archiving change add-gui-manager-system-skill. Update Purpose after archive.
## Requirements
### Requirement: GUI Manager Operator Skill
The core public pack SHALL preserve `isomer-op-gui-mgr` as protected member `gui` for Project Web GUI lifecycle guidance, backend API reference, and troubleshooting.

#### Scenario: GUI manager member exists
- **WHEN** packaged core skills are inspected
- **THEN** `operator/isomer-op-entrypoint/subskills/isomer-op-gui-mgr/SKILL.md` exists
- **AND** its folder and frontmatter retain logical id `isomer-op-gui-mgr`
- **AND** its UI metadata version is release-aligned

#### Scenario: GUI manager is command-style
- **WHEN** the protected GUI member is inspected
- **THEN** it defines default help and bounded launch, status, API-reference, refresh, and troubleshooting routines
- **AND** it loads only the selected detail page for one bounded operation

#### Scenario: Public entrypoint owns GUI routing
- **WHEN** a user asks to start, restart, inspect, debug, refresh, or diagnose Project Web GUI
- **THEN** `$isomer-op-entrypoint use gui to <task>` routes to `isomer-op-entrypoint->gui`
- **AND** the request is not routed first to another owner unless its actual subject is Project initialization, Topic Workspace repair, or service support

#### Scenario: GUI manager is not top-level
- **WHEN** ordinary core host discovery runs
- **THEN** it does not list `isomer-op-gui-mgr` as an independent public skill

### Requirement: GUI Manager Discoverability
GUI management SHALL be discoverable through public core help, route-by-task behavior, and protected member metadata.

#### Scenario: Public help lists GUI route
- **WHEN** `isomer-op-entrypoint` help is shown
- **THEN** it lists public subcommand `gui` and a concise purpose
- **AND** it does not require users to know the protected logical id

#### Scenario: Internal catalog lists capability
- **WHEN** pack metadata is queried
- **THEN** it reports logical id `isomer-op-gui-mgr`, member `gui`, nested path, and invocation designator

### Requirement: GUI Lifecycle Guidance
`isomer-op-gui-mgr` SHALL describe the supported local GUI Backend lifecycle commands and cache-mode choices.

#### Scenario: Launch guidance uses global CLI
- **WHEN** GUI manager launch guidance is inspected
- **THEN** it uses `isomer-cli project web serve --root <project-root>` as the canonical start command
- **AND** it does not instruct installed operators to run Isomer's own CLI through `pixi run`

#### Scenario: Launch options are documented
- **WHEN** GUI manager launch guidance is inspected
- **THEN** it explains `--host`, `--port`, `--reload`, `--no-browser`, and `--cache-mode normal|debug`
- **AND** it identifies normal cache mode as the ordinary launch mode
- **AND** it identifies debug cache mode as the mode for avoiding browser cache interference while debugging

#### Scenario: Lifecycle guidance stays local
- **WHEN** GUI manager lifecycle guidance is inspected
- **THEN** it presents the GUI Backend as a local single-user service for one selected Project root per process
- **AND** it does not claim daemon, supervisor, remote deployment, authentication, or canonical research-state ownership beyond existing Project Web behavior

### Requirement: GUI Backend API Reference Guidance
`isomer-op-gui-mgr` SHALL provide a concise backend API reference for existing Project Web route families and direct detailed payload questions to UI contract documentation.

#### Scenario: API reference lists route families
- **WHEN** GUI manager API reference guidance is inspected
- **THEN** it lists health, Project summary, topic list, Project explorer, openable descriptors, topic detail, runtime, overview, actors, records, records export, graphs, recent errors, events, record detail, idea detail, record viewer, rendered Markdown, record lineage, siblings, files, facets, and index maintenance route families
- **AND** it marks read-only route families separately from explicit mutation route families such as index rebuild or cleanup

#### Scenario: API reference points to UI contracts
- **WHEN** GUI manager API reference guidance describes payload shapes consumed by the frontend
- **THEN** it points to `docs/ui/contracts/` as the detailed GUI payload contract source
- **AND** it does not embed full response schemas that duplicate those contract docs

#### Scenario: API reference preserves canonical-state boundary
- **WHEN** GUI manager API reference guidance explains GUI Backend APIs
- **THEN** it states that the GUI Backend reads Project, Topic Workspace, Workspace Runtime, query-index, and payload-file state
- **AND** it states that the GUI Backend does not own canonical research state

### Requirement: GUI Troubleshooting and Refresh Guidance
`isomer-op-gui-mgr` SHALL guide safe troubleshooting for slow loads, stale UI data, cache problems, non-interpretable topic data, and query-index maintenance.

#### Scenario: Troubleshooting distinguishes refresh types
- **WHEN** GUI manager troubleshooting guidance is inspected
- **THEN** it distinguishes browser refresh, debug cache-mode restart, topic change events, read-only recent-errors queries, index validation, explicit index rebuild, and explicit index cleanup
- **AND** it does not present frontend refresh as canonical record repair

#### Scenario: Recent errors are queryable
- **WHEN** GUI manager troubleshooting guidance covers non-interpretable graph, timeline, or record data
- **THEN** it directs operators to the Project Web recent-errors API or GUI surface
- **AND** it describes recent errors as bounded service-local diagnostics rather than durable Workspace Runtime records

#### Scenario: Unsafe repairs route to owners
- **WHEN** troubleshooting discovers invalid Project configuration, Topic Workspace storage problems, record schema problems, or code-level GUI defects
- **THEN** the GUI manager guidance routes Project configuration work to `isomer-op-project-mgr`
- **AND** it routes initialized-topic storage or package/environment work to `isomer-op-topic-mgr`
- **AND** it reports code-level defects as repository development work rather than attempting hidden runtime repair

### Requirement: GUI Manager Output Contract
`isomer-op-gui-mgr` SHALL report GUI operation results with a concise operator-oriented output contract.

#### Scenario: Essential output is defined
- **WHEN** the GUI manager skill is inspected
- **THEN** it defines Essential Output fields for status, project, service URL or route family, cache mode, commands or API routes used, diagnostics, blockers, and next action

#### Scenario: Complete output is available
- **WHEN** the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output
- **THEN** GUI manager guidance includes fuller details such as resolved Project root, selected topic, backend process command, route family, response summary, cache headers or mode, recent-errors summary, index action, diagnostics, and handoff route


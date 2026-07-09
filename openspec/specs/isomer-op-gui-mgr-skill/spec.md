# isomer-op-gui-mgr-skill Specification

## Purpose
TBD - created by archiving change add-gui-manager-system-skill. Update Purpose after archive.
## Requirements
### Requirement: GUI Manager Operator Skill
The packaged operator skillset SHALL include `isomer-op-gui-mgr` as the user-facing operator skill for Project Web GUI lifecycle guidance, backend API reference, and GUI troubleshooting.

#### Scenario: GUI manager skill exists
- **WHEN** packaged operator system skills are inspected
- **THEN** `operator/isomer-op-gui-mgr/SKILL.md` exists
- **AND** the skill frontmatter name is `isomer-op-gui-mgr`
- **AND** `operator/isomer-op-gui-mgr/agents/openai.yaml` uses `isomer-op-gui-mgr` as its display name

#### Scenario: GUI manager is command-style
- **WHEN** the GUI manager skill is inspected
- **THEN** it defines a default help workflow
- **AND** it lists bounded subcommands or reference pages for launch, status, backend API reference, record refresh or index maintenance, and troubleshooting
- **AND** the top-level skill instructs agents to load only the selected reference page for one bounded GUI operation

#### Scenario: GUI manager owns GUI operation routing
- **WHEN** a Project Operator asks how to start, restart, inspect, debug, refresh, or diagnose the Project Web GUI
- **THEN** operator routing identifies `isomer-op-gui-mgr` as the owning user-facing skill
- **AND** it does not route that request first to Project Manager, Topic Manager, or a service skill unless the request is actually about Project initialization, Topic Workspace repair, or lower-level service support

### Requirement: GUI Manager Discoverability
The packaged operator routing surfaces SHALL expose `isomer-op-gui-mgr` from both informed-user dispatch and read-only welcome menus.

#### Scenario: Entrypoint routes GUI requests
- **WHEN** `isomer-op-entrypoint` routing references are inspected
- **THEN** the system skill index lists `isomer-op-gui-mgr` as an active operator skill
- **AND** it maps Project Web GUI lifecycle, cache-mode debugging, GUI refresh, backend API reference, recent-errors inspection, and GUI troubleshooting requests to `isomer-op-gui-mgr`

#### Scenario: Welcome options include GUI manager
- **WHEN** `isomer-op-welcome` option-menu references are inspected
- **THEN** `show-options` lists Project Web GUI lifecycle, refresh, troubleshooting, or backend API reference as a supported action
- **AND** it names `isomer-op-gui-mgr` as the owner skill

#### Scenario: Welcome skill map includes GUI manager
- **WHEN** `isomer-op-welcome` skill-map references are inspected
- **THEN** `show-skill-map` includes `isomer-op-gui-mgr` in the active owner-skill map
- **AND** it gives direct invocation language such as `Use $isomer-op-gui-mgr help` or a GUI Manager subcommand

#### Scenario: Welcome path choice can select GUI manager
- **WHEN** `isomer-op-welcome` path-choice guidance is inspected
- **THEN** `choose-path` prefers `isomer-op-gui-mgr` for GUI Backend lifecycle, Project Web cache/debug, backend API reference, recent-errors, and GUI refresh questions
- **AND** it still routes Project setup to Project Manager and initialized-topic repair to Topic Manager

#### Scenario: Welcome help names GUI manager
- **WHEN** `isomer-op-welcome` help references are inspected
- **THEN** `help` names `isomer-op-gui-mgr` with the active owner skills
- **AND** it describes the skill as the owner for Project Web GUI lifecycle and backend API guidance

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


## MODIFIED Requirements

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

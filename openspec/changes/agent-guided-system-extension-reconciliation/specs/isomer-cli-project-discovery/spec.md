## ADDED Requirements

### Requirement: Direct Project Initialization Does Not Discover Agent Skill Roots
`isomer-cli project init` SHALL remain independent of provider-specific skill discovery and SHALL not register extensions from inferred project or user roots.

#### Scenario: Direct init has no agent inventory
- **WHEN** a user invokes `isomer-cli project init` directly
- **THEN** the command initializes Project-owned state without assuming which agent host is the operator
- **AND** it does not scan conventional Claude, Codex, Kimi, generic, plugin, or user-home skill roots

#### Scenario: Direct init writes no inferred declarations
- **WHEN** system skills or receipts happen to exist under directories near the new Project
- **THEN** direct initialization does not add their extension ids to the Project Manifest
- **AND** operator-skill reconciliation remains a separate higher-level step

#### Scenario: Explicit observations use explicit roots
- **WHEN** a Project-facing read-only command reports skill-root observations
- **THEN** each observed root was supplied explicitly by the caller
- **AND** root contents are interpreted through the Isomer-owned internal inspection contract

### Requirement: Project Extension Detection Does Not Guess Default Roots
Project-scoped extension detection SHALL accept explicit skill roots or remain catalog-and-declaration-only rather than searching provider locations by default.

#### Scenario: No explicit roots performs no filesystem scan
- **WHEN** Project extension detection is invoked without explicit skill roots
- **THEN** it reports Project declarations and catalog state without scanning filesystem roots
- **AND** it advises operator-guided detection when installation evidence is needed

#### Scenario: Explicit roots are independently reported
- **WHEN** one or more explicit skill roots are supplied
- **THEN** detection delegates each root to the internal explicit-root inspector
- **AND** it keeps results separated by supplied root without selecting a Project-wide operator target

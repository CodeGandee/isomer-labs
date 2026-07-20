## MODIFIED Requirements

### Requirement: Production Kaoju Skill Family
The package SHALL provide a self-contained production Kaoju pack with independent public welcome and execution entrypoint bundles plus the existing protected `isomer-kaoju-<purpose>` capabilities.

#### Scenario: Kaoju public pair exists
- **WHEN** packaged Kaoju assets are inspected
- **THEN** sibling bundles `isomer-ext-kaoju-welcome` and `isomer-ext-kaoju-entrypoint` contain valid public skill metadata
- **AND** the thirteen current Kaoju capabilities remain protected below the entrypoint

#### Scenario: Kaoju welcome is self-contained
- **WHEN** `isomer-ext-kaoju-welcome` is copied or linked as part of the pack
- **THEN** it resolves its active typical-use-case and command-map resources without loading private files from the entrypoint or protected subskills
- **AND** it may reference public entrypoint invocation names without becoming an execution owner

#### Scenario: Shared machine contracts remain package-owned
- **WHEN** welcome or entrypoint needs current Kaoju command or process metadata
- **THEN** checked machine contracts remain owned by the installed Kaoju Python package and manifest
- **AND** welcome does not introduce a second survey-process registry

### Requirement: Kaoju Pipeline Command Surface
`isomer-ext-kaoju-entrypoint` SHALL remain the single Kaoju execution entrypoint, and `isomer-ext-kaoju-welcome` SHALL provide a separate read-only teaching surface for its survey intents, compatibility procedures, and grouped managers.

#### Scenario: Concrete Kaoju task uses entrypoint
- **WHEN** a user requests reading-list work, source ingestion, direction selection, comparison, code preparation, trial execution, paper production, or wiki export
- **THEN** `isomer-ext-kaoju-entrypoint` selects and executes the applicable public command or protected capability
- **AND** existing interaction, evidence, Gate, checkpoint, and terminal contracts remain in force

#### Scenario: Newcomer asks how to use Kaoju
- **WHEN** a user asks what Kaoju is designed for, which procedure fits, or how to form a request
- **THEN** `isomer-ext-kaoju-welcome` presents curated typical use cases and exact entrypoint examples
- **AND** it does not run a Kaoju manager or research procedure

#### Scenario: Historical pipeline identity is used
- **WHEN** compatibility lookup encounters `isomer-kaoju-pipeline`
- **THEN** it resolves to `isomer-ext-kaoju-entrypoint`
- **AND** it does not resolve to the welcome skill

#### Scenario: Nested manager form is taught
- **WHEN** welcome explains a grouped manager or nested subcommand such as paper-template management
- **THEN** it shows the accepted public entrypoint command form and representative task
- **AND** it does not expose internal object-generator notation as the ordinary user invocation

## ADDED Requirements

### Requirement: Kaoju Welcome Maps the Complete Public Command Inventory
The Kaoju welcome skill SHALL maintain a manifest-validated command map and curated use-case guide for the current Kaoju public entrypoint.

#### Scenario: Command map is validated
- **WHEN** Kaoju welcome validation runs
- **THEN** every current public survey-intent, compatibility-procedure, manager, and help command appears exactly once
- **AND** missing, duplicate, extra, or stale command ids fail validation

#### Scenario: Typical use cases are curated
- **WHEN** default Kaoju welcome output is inspected
- **THEN** it prioritizes landscape discovery, reading-list work, evidence intake, comparison, trials, paper production, and wiki export
- **AND** it does not dump the complete command inventory before offering those representative patterns

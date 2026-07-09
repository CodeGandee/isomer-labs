# operator-system-extension-declarations Specification

## Purpose
TBD - created by archiving change catalog-callback-insertion-points. Update Purpose after archive.
## Requirements
### Requirement: Project Manifest Declares Operator System Extensions
The system SHALL store user-declared Project operator system extensions in the Project Manifest without claiming that Isomer has verified manually installed operator skill files.

#### Scenario: Project Manifest stores declared extensions
- **WHEN** a Project Manifest declares operator system extensions
- **THEN** the declarations are stored as stable extension ids under the Project Manifest operator system-extension configuration
- **AND** the declarations are interpreted as user-declared operator state rather than verified filesystem state

#### Scenario: Missing declarations are empty
- **WHEN** a Project Manifest has no operator system-extension declaration
- **THEN** the system treats the Project as having no optional operator system extensions declared
- **AND** core system skills remain available by catalog rule

#### Scenario: Unknown extension id is rejected
- **WHEN** a user attempts to record an operator system extension id that is not declared as an optional packaged system extension in the system-skill catalog
- **THEN** the system rejects the request with a deterministic diagnostic that names the unknown extension id
- **AND** the Project Manifest is not modified by that failed request

### Requirement: Project System Extension CLI
The system SHALL expose Project-scoped CLI operations for listing known system extensions and remembering or forgetting user-declared operator system extensions.

#### Scenario: List reports catalog and Project declaration state
- **WHEN** a user runs `isomer-cli project system-extensions list`
- **THEN** the command reports known optional system extension ids from the packaged system-skill catalog
- **AND** the command reports whether each extension id is declared installed in the selected Project Manifest
- **AND** the command does not inspect or modify Project operator skill files

#### Scenario: Remember records an extension
- **WHEN** a user runs `isomer-cli project system-extensions remember <extension-id>` for a known optional system extension
- **THEN** the command records the extension id in the Project Manifest operator system-extension declarations
- **AND** repeated remember operations for the same extension id are idempotent

#### Scenario: Forget removes an extension declaration
- **WHEN** a user runs `isomer-cli project system-extensions forget <extension-id>`
- **THEN** the command removes the extension id from the Project Manifest operator system-extension declarations when present
- **AND** the command does not remove callback registries, Toolbox configuration, packaged assets, or manually installed operator skill files

#### Scenario: JSON output states verification boundary
- **WHEN** a user runs a Project system-extension command in JSON mode
- **THEN** the output includes deterministic extension ids, catalog metadata, Project declaration state, and an indication that optional extension installation is user-declared rather than filesystem-verified


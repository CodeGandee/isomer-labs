# operator-system-extension-declarations Specification

## Purpose
TBD - created by archiving change catalog-callback-insertion-points. Update Purpose after archive.
## Requirements

### Requirement: Project Manifest Declares Operator System Extensions
The system SHALL store Project operator system extensions as authoritative claimed Project state without claiming that every current operator environment has been filesystem-verified.

#### Scenario: Project Manifest stores declared extensions
- **WHEN** a user or authorized operator workflow declares operator system extensions
- **THEN** the declarations are stored as stable extension ids under the Project Manifest operator system-extension configuration
- **AND** the declarations are interpreted as authoritative Project state rather than a guarantee about every agent host or skill root

#### Scenario: Missing declarations are empty
- **WHEN** a Project Manifest has no operator system-extension declaration
- **THEN** the system treats the Project as having no optional operator system extensions declared
- **AND** core system skills remain available by catalog rule

#### Scenario: Unknown extension id is rejected
- **WHEN** a user or operator workflow attempts to record an operator system extension id that is not declared as an optional packaged system extension in the system-skill catalog
- **THEN** the system rejects the request with a deterministic diagnostic that names the unknown extension id
- **AND** the Project Manifest is not modified by that failed request

#### Scenario: Declaration is trusted before discovery
- **WHEN** an operator resolves extension availability and the Project already declares the extension
- **THEN** it trusts the declaration before consulting receipts or live inventory
- **AND** later unavailability is reported as stale or inconsistent user-controlled state

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

### Requirement: Project Manifest Declares Houmao Integration Policy
The Project Manifest SHALL support explicit Houmao integration policy separate from user-declared operator system extension installation state.

#### Scenario: Houmao integration state is stored separately
- **WHEN** the Project records Houmao integration policy
- **THEN** it stores the policy under an operator integration configuration for Houmao
- **AND** it does not rely solely on `operator.system_extensions.installed` to decide whether Houmao-backed operations may run

#### Scenario: Disabled policy skips operations
- **WHEN** the Project Manifest declares Houmao integration disabled
- **THEN** Houmao-aware Isomer operations skip Houmao-related work with a deterministic skip status
- **AND** they do not require projected Houmao skill files, Houmao credentials, or a successful `houmao-mgr` preflight

#### Scenario: Enablement can be recorded idempotently
- **WHEN** a user or setup workflow enables Houmao integration for a Project
- **THEN** the Project Manifest records the enabled state idempotently
- **AND** repeated enable operations preserve existing configured skill root and Houmao Project path values unless an explicit replacement option is used

#### Scenario: Disablement does not delete state
- **WHEN** a user disables Houmao integration for a Project
- **THEN** the Project Manifest records the disabled state
- **AND** the command does not delete `.isomer-labs/.houmao/`, `.isomer-labs/houmao-skills/`, Topic Workspace material, or runtime records\n

### Requirement: Operator-Managed Extension Registration Is Idempotent
Project extension declarations SHALL support additive bookkeeping by authorized operator skills without requiring direct CLI initialization or low-level installation to infer agent context.

#### Scenario: Operator remembers discovered extension
- **WHEN** an operator skill establishes a complete extension from managed receipt or live inventory evidence during an authorized mutation workflow
- **THEN** it can call the existing Project remember operation
- **AND** repeated registration remains idempotent

#### Scenario: Direct inspection never registers
- **WHEN** a user runs a read-only internal inspection or direct Project extension detection command
- **THEN** the command does not add declarations automatically

#### Scenario: Reconciliation never auto-forgets
- **WHEN** one working agent lacks a Project-declared extension
- **THEN** automated reconciliation preserves the declaration
- **AND** only an explicit forget request removes it

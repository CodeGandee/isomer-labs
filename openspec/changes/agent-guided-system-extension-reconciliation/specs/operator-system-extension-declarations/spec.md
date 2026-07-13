## MODIFIED Requirements

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

## ADDED Requirements

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

## ADDED Requirements

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
- **AND** the command does not delete `.isomer-labs/.houmao/`, `.isomer-labs/houmao-skills/`, Topic Workspace material, or runtime records


# isomer-op-system-skill-mgr-skill Specification

## Purpose
TBD - created by archiving change agent-guided-system-extension-reconciliation. Update Purpose after archive.

## Requirements

### Requirement: System Skill Manager Bundle
The repository SHALL provide a core operator skill named `isomer-op-system-skill-mgr` that owns working-agent system-skill detection, reconciliation, installation, status, and repair.

#### Scenario: Skill bundle is complete
- **WHEN** the packaged operator skillset is inspected
- **THEN** it contains `operator/isomer-op-system-skill-mgr/SKILL.md`, `agents/openai.yaml`, and directly linked local references needed to execute its workflow
- **AND** its frontmatter and interface metadata use the same skill name

#### Scenario: Owner subcommands are available
- **WHEN** the skill's help or local command index is inspected
- **THEN** it exposes `detect-extensions`, `reconcile-extensions`, `install-extension`, `status`, and `repair` subcommands
- **AND** each subcommand preserves read-only or mutation posture explicitly

### Requirement: System Skill Manager Uses Ordered Extension Evidence
The system-skill manager SHALL resolve optional extensions from Project declaration, explicit project-root receipt, and live inventory evidence in that order.

#### Scenario: Project declaration wins
- **WHEN** the Project Manifest declares an extension
- **THEN** the manager trusts that declaration and does not require receipt or inventory confirmation before routing
- **AND** it reports later load or execution failure as stale user-controlled state rather than silently removing the declaration

#### Scenario: Receipt-backed fallback uses host-known roots
- **WHEN** an undeclared extension may exist in a project-scope root known to the working agent
- **THEN** the manager passes that explicit root to `internals inspect-system-skill-root`
- **AND** it does not teach or guess provider-specific root names, receipt filenames, or receipt schemas

#### Scenario: Live inventory covers ambient installations
- **WHEN** no declaration or complete managed project receipt establishes the extension
- **THEN** the manager passes the host-visible inventory to `internals classify-system-skill-inventory`
- **AND** complete inventory evidence can represent user-home, plugin, environment-owned, or other host-discovered installations

#### Scenario: No evidence reports unknown
- **WHEN** all three evidence levels fail to establish an extension
- **THEN** the manager reports the extension as unknown or missing and offers its installation subcommand

### Requirement: System Skill Reconciliation Is Additive
The system-skill manager SHALL register complete receipt-backed or live-inventory extensions during authorized operator mutation workflows unless the user opts out.

#### Scenario: Reconciliation remembers complete extension
- **WHEN** `reconcile-extensions` finds a complete extension that the Project does not declare
- **THEN** it runs the idempotent Project extension registration primitive
- **AND** it reports the extension id and evidence basis used for registration

#### Scenario: Detection-only request does not mutate
- **WHEN** the user requests detection, status, help, or explicitly opts out of registration
- **THEN** the manager does not call Project extension registration
- **AND** it reports registration advice separately

#### Scenario: Missing current inventory never forgets declaration
- **WHEN** a declared extension is absent from the current agent's roots or live inventory
- **THEN** reconciliation preserves the declaration
- **AND** it does not infer that other operator environments lack the extension

### Requirement: Operator-Managed Extension Installation Converges
The system-skill manager SHALL combine a user-authorized extension installation with verification, Project registration, and activation guidance.

#### Scenario: Successful installation is registered
- **WHEN** `install-extension <extension-id>` installs a complete family into a root selected from host-known operator context
- **THEN** the manager verifies the result with safe CLI primitives
- **AND** it remembers the extension in the selected Project unless the user opted out

#### Scenario: Registration failure is partial
- **WHEN** installation succeeds but Project registration fails
- **THEN** the manager reports a non-success partial outcome that distinguishes installed files from missing registration
- **AND** a retry can complete registration without reinstalling the extension

#### Scenario: New installation may require host refresh
- **WHEN** installation succeeds but the extension is not observable in a refreshed live inventory
- **THEN** the manager reports `host_refresh_required`
- **AND** it advises a new turn, thread, or host-native refresh without claiming current-session availability

### Requirement: System Skill Manager Validation
Repository validation SHALL enforce the system-skill manager's owner boundary and required workflow material.

#### Scenario: Validator accepts complete manager
- **WHEN** operator and packaged-skill validation run against a complete system-skill manager bundle
- **THEN** validation accepts its frontmatter, interface metadata, local references, subcommands, trust order, mutation rules, and global `isomer-cli` guidance

#### Scenario: Validator rejects provider path hard-coding
- **WHEN** manager workflow text treats one provider-specific project or user-home path as universal discovery authority
- **THEN** validation reports a missing provider-neutral explicit-root or live-inventory boundary

## MODIFIED Requirements

### Requirement: Domain Agent Team Template Registration
The system SHALL discover and register reusable Domain Agent Team Templates without treating them as Topic Agent Team Profiles, Agent Team Instances, Topic Workspaces, provider-specific launch packages, or implicit Isomer core package assets.

#### Scenario: Core package has no implicit built-in templates
- **WHEN** a Project asks Isomer to list available Domain Agent Team Templates without Project-local registrations or configured Team Repositories
- **THEN** the system does not include `deepsci-org`, `deepsci-mini`, or any other template solely because the `isomer_labs` Python package is installed

#### Scenario: Project manifest template refs are loaded
- **WHEN** the Project Manifest declares a Domain Agent Team Template ref with a project-scoped source path
- **THEN** the system loads that ref as a reusable template candidate without copying template files into a Topic Workspace

#### Scenario: Team Repository template refs are loaded
- **WHEN** a configured Team Repository declares an active Domain Agent Team Template ref
- **THEN** the system loads that ref as a reusable template candidate with Team Repository source provenance

#### Scenario: Template path outside project is rejected unless resolved through Team Repository
- **WHEN** a Project Manifest declares a non-Team-Repository Domain Agent Team Template source outside the Project root
- **THEN** validation reports a Project Manifest diagnostic and does not register that template

### Requirement: Template Package Validation
The system SHALL validate the generated package shape and Isomer template boundary for each registered Domain Agent Team Template, regardless of whether it comes from a Project-local registration or a configured Team Repository.

#### Scenario: Team Repository deepsci-org execplan package validates
- **WHEN** a configured Team Repository provides the `deepsci-org` Domain Agent Team Template
- **THEN** validation checks `manifest.toml`, participant contracts, role profiles, notifier prompts, generated skills, harness schemas, workspace contract, state contract, and run contract

#### Scenario: Missing package artifact is reported
- **WHEN** a registered Domain Agent Team Template references a missing manifest, participant contract, role profile, generated skill, harness schema, workspace contract, state contract, or run contract
- **THEN** validation reports a diagnostic naming the missing artifact path and the Domain Agent Team Template ref

#### Scenario: Harness validation contributes diagnostics
- **WHEN** the generated harness validation command is available and reports failures
- **THEN** the system includes those failures in template diagnostics without treating the harness as the only source of Isomer validation truth

### Requirement: Template CLI Inspection
The system SHALL expose deterministic CLI inspection and validation for registered Domain Agent Team Templates.

#### Scenario: Template list command reports registered templates
- **WHEN** a user runs `isomer-cli project team-templates list`
- **THEN** the output includes each registered Domain Agent Team Template id, source kind, source path when available, Team Repository provenance when applicable, and validation status

#### Scenario: Empty template list explains external team sources
- **WHEN** a user runs `isomer-cli project team-templates list` without Project-local templates or configured Team Repositories
- **THEN** the output reports an empty template list and explains that reusable Agent Team definitions are supplied by Project registrations or external Team Repositories

#### Scenario: Template inspect command reports template structure
- **WHEN** a user runs `isomer-cli project team-templates inspect <template-id>` for a Project-local or Team Repository template
- **THEN** the output includes reusable Agent Roles, Workflow Stages, required and optional skills, template parameters, generated package artifact paths, and source metadata

#### Scenario: Template validate command reports Isomer diagnostics
- **WHEN** a user runs `isomer-cli project team-templates validate <template-id>` for a Project-local or Team Repository template
- **THEN** the command reports stable Isomer diagnostics and deterministic JSON output when requested

### Requirement: Milestone Template Completion Verification
The system SHALL verify Domain Agent Team Template registration and validation with configured Team Repository templates and project-local fixture templates before template-related milestones are marked complete.

#### Scenario: Project-local template fixture validates
- **WHEN** a Project Manifest registers a minimal project-local Domain Agent Team Template fixture with structurally valid manifest, participant, binding, workspace, state, run, skill, and schema artifacts
- **THEN** `isomer-cli project team-templates validate <template-id>` validates that template without relying on `deepsci-org`-specific role ids

#### Scenario: Team Repository template fixture validates
- **WHEN** a test configures a Team Repository containing `deepsci-org` or `deepsci-mini`
- **THEN** `isomer-cli project team-templates list`, `inspect`, and `validate` can use those templates through Team Repository discovery rather than core built-in registration

#### Scenario: Missing project-local template artifact is rejected
- **WHEN** a project-local Domain Agent Team Template fixture references a missing manifest, participant contract, role profile, generated skill, harness schema, workspace contract, state contract, or run contract
- **THEN** validation reports an Isomer diagnostic naming the missing artifact path and template ref

#### Scenario: Project-local template boundary leak is rejected
- **WHEN** a project-local Domain Agent Team Template fixture contains a concrete Research Topic, Topic Workspace, Topic Agent Team Profile, Agent Team Instance, mailbox, gateway, credential, launch, or Run truth value instead of an allowed placeholder
- **THEN** validation rejects the template as crossing the template boundary

### Requirement: deepsci-org Completion Evidence
The system SHALL keep `deepsci-org` usable as seed Team Repository content while proving its generated package remains reusable, placeholder-bound, and independent of Topic Workspace state.

#### Scenario: Team Repository deepsci-org validates through public CLI
- **WHEN** the validation suite configures a Team Repository containing `deepsci-org`
- **THEN** it validates `deepsci-org` through `isomer-cli project team-templates list`, `isomer-cli project team-templates inspect deepsci-org`, and `isomer-cli project team-templates validate deepsci-org`

#### Scenario: deepsci-org role expectations stay scoped to Team Repository deepsci-org
- **WHEN** validation inspects the `deepsci-org` template resolved from a Team Repository
- **THEN** it enforces the seven expected `deepsci-org` role ids, scalable `experimenter` and `analyzer` metadata, required skills, optional skills, Capability Binding placeholders, and Skill Binding Projection placeholders

#### Scenario: Generic templates are not forced into deepsci role ids
- **WHEN** validation inspects a non-`deepsci-org` project-local or Team Repository Domain Agent Team Template fixture
- **THEN** it validates generic Agent Role, Workflow Stage, artifact, and boundary shape without requiring the seven `deepsci-org` role ids

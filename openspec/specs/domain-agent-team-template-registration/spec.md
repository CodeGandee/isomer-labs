# domain-agent-team-template-registration Specification

## Purpose
Define how Isomer discovers, registers, validates, and inspects reusable Domain Agent Team Templates, starting with the repository-local `deepsci-org` template.
## Requirements
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

### Requirement: Template Boundary Protection
The system SHALL preserve the boundary between reusable template facts and topic-specific or runtime facts.

#### Scenario: Topic placeholders are allowed at template layer
- **WHEN** the `deepsci-org` Domain Agent Team Template contains placeholders for Research Topic, Topic Workspace, Workspace Runtime, Topic Agent Team Profile, Capability Binding, Skill Binding Projection, policy, provider, or Agent Workspace refs
- **THEN** template validation accepts those placeholders as unresolved template parameters

#### Scenario: Concrete topic refs are rejected at template layer
- **WHEN** a Domain Agent Team Template contains concrete Research Topic ids, Topic Workspace paths, Topic Agent Team Profile ids, Agent Team Instance ids, mailbox refs, gateway refs, credentials, live process ids, Run state, or command outputs
- **THEN** validation rejects the template material as crossing the template boundary

#### Scenario: Template does not create workspace-local teams
- **WHEN** a template workspace contract says concrete work belongs in a Topic Workspace
- **THEN** validation confirms that the template does not require a `teams/` directory inside any Topic Workspace

### Requirement: Role and Workflow Stage Mapping
The system SHALL map Domain Agent Team Template roles and Workflow Stages into neutral Isomer concepts.

#### Scenario: deepsci-org roles are mapped
- **WHEN** the system inspects the `deepsci-org` template participant contract
- **THEN** it maps `deepsci-org-master`, `deepsci-org-framer`, `deepsci-org-designer`, `deepsci-org-experimenter`, `deepsci-org-analyzer`, `deepsci-org-publisher`, and `deepsci-org-reviewer` to Agent Role definitions with role kind, required status, scalability, required skills, optional skills, Capability Binding slots, and Skill Binding Projection slots

#### Scenario: Workflow stage ownership is mapped
- **WHEN** the system inspects `deepsci-org` stage routes
- **THEN** it records each Workflow Stage owner role and alternate owner role without creating Run state or Workflow Stage Cursor state

#### Scenario: Scalable role metadata is preserved
- **WHEN** `deepsci-org-experimenter` or `deepsci-org-analyzer` is marked scalable for Research Task scope
- **THEN** the template record preserves that task-level fanout capability for later Topic Agent Team Profile validation

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

### Requirement: Template Completion Roadmap Gate
The system SHALL mark Milestone 2 complete only after template registration, validation, CLI, fixture, documentation, and OpenSpec validation gates pass.

#### Scenario: Milestone 2 roadmap items are marked after validation
- **WHEN** template fixture tests, built-in `deepsci-org` tests, `openspec validate --all`, lint, typecheck, unit tests, and research skill validation all pass
- **THEN** the Milestone 2 checklist in `ROADMAP.md` is marked complete

### Requirement: Template Instantiation Metadata Inspection
The system SHALL expose instantiation metadata for Domain Agent Team Templates without treating the template as a concrete topic team.

#### Scenario: Placeholder catalog is reported
- **WHEN** a user, Project Operator Session, Operator Agent, or Topic Service Agent inspects a Domain Agent Team Template
- **THEN** the output includes declared placeholder names, required status, source files, expected replacement layer, and whether unresolved values block profile save or only launch

#### Scenario: Role binding slots are reported
- **WHEN** a user, Project Operator Session, Operator Agent, or Topic Service Agent inspects a Domain Agent Team Template
- **THEN** the output includes role ids, required or optional status, Agent Profile slots, Capability Binding slots, Skill Binding Projection slots, Agent Workspace placeholder refs, and Workflow Stage ownership

#### Scenario: Instantiation schema is discoverable
- **WHEN** a template package includes an instantiation schema or placeholder parameter catalog
- **THEN** template validation and inspection expose that schema path and validate that it does not contain concrete Research Topic, Topic Workspace, Agent Team Instance, launch, credential, or Run truth

### Requirement: Template Boundary for Agent-Mediated Instantiation
The system SHALL preserve the reusable template boundary when instantiation metadata is added for Project Operator Session, Operator Agent, or Topic Service Agent workflows.

#### Scenario: Template may require topic instantiation
- **WHEN** a Domain Agent Team Template declares `topic_instantiation_required`
- **THEN** the system accepts the declaration and reports that the template must go through Topic Team Specialization before Agent Team Instance creation

#### Scenario: Template validation rejects concrete packet output
- **WHEN** a Domain Agent Team Template source file contains an approved instantiation packet, concrete Topic Agent Team Profile Bundle, concrete Agent Workspace path, live adapter ref, user approval decision, or Topic Service Agent runtime ref
- **THEN** template validation rejects the file as crossing from template material into topic, service, or runtime material

#### Scenario: Template source is copied before topic edits
- **WHEN** a Project Operator Session, Operator Agent, or Topic Service Agent needs to rewrite prompts, skills, workflow contracts, or execplan material for a topic
- **THEN** the system copies the required template material into the Topic Agent Team Profile Bundle and applies topic edits there rather than editing the Domain Agent Team Template source


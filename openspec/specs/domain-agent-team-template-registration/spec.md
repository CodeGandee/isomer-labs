# domain-agent-team-template-registration Specification

## Purpose
Define how Isomer discovers, registers, validates, and inspects reusable Domain Agent Team Templates, starting with the repository-local `deepsci-org` template.

## Requirements
### Requirement: Domain Agent Team Template Registration
The system SHALL discover and register reusable Domain Agent Team Templates without treating them as Topic Agent Team Profiles, Agent Team Instances, Topic Workspaces, or provider-specific launch packages.

#### Scenario: Built-in deepsci-org template is discoverable
- **WHEN** a Project asks Isomer to list available Domain Agent Team Templates
- **THEN** the system includes the `deepsci-org` template sourced from `teams/deepsci-org/execplan/`

#### Scenario: Project manifest template refs are loaded
- **WHEN** the Project Manifest declares a Domain Agent Team Template ref with a project-scoped source path
- **THEN** the system loads that ref as a reusable template candidate without copying template files into a Topic Workspace

#### Scenario: Template path outside project is rejected unless built-in
- **WHEN** a Project Manifest declares a non-built-in Domain Agent Team Template source outside the Project root
- **THEN** validation reports a Project Manifest diagnostic and does not register that template

### Requirement: Template Package Validation
The system SHALL validate the generated package shape and Isomer template boundary for each registered Domain Agent Team Template.

#### Scenario: deepsci-org execplan package validates
- **WHEN** the system validates the `deepsci-org` Domain Agent Team Template
- **THEN** validation checks `manifest.toml`, participant contracts, role profiles, notifier prompts, generated skills, harness schemas, workspace contract, state contract, and run contract

#### Scenario: Missing package artifact is reported
- **WHEN** a registered Domain Agent Team Template references a missing manifest, participant contract, role profile, generated skill, harness schema, workspace contract, state contract, or run contract
- **THEN** validation reports a diagnostic naming the missing artifact path and the Domain Agent Team Template ref

#### Scenario: Harness validation contributes diagnostics
- **WHEN** the generated `deepsci-org` harness validation command is available and reports failures
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
- **WHEN** a user runs `isomer-cli team-templates list`
- **THEN** the output includes each registered Domain Agent Team Template id, source kind, source path when available, and validation status

#### Scenario: Template inspect command reports template structure
- **WHEN** a user runs `isomer-cli team-templates inspect deepsci-org`
- **THEN** the output includes reusable Agent Roles, Workflow Stages, required and optional skills, template parameters, generated package artifact paths, and source metadata

#### Scenario: Template validate command reports Isomer diagnostics
- **WHEN** a user runs `isomer-cli team-templates validate deepsci-org`
- **THEN** the command reports stable Isomer diagnostics and deterministic JSON output when requested

## ADDED Requirements

### Requirement: Milestone Template Completion Verification
The system SHALL verify Domain Agent Team Template registration and validation with both the built-in `deepsci-org` template and project-local fixture templates before Milestone 2 is marked complete.

#### Scenario: Project-local template fixture validates
- **WHEN** a Project Manifest registers a minimal project-local Domain Agent Team Template fixture with structurally valid manifest, participant, binding, workspace, state, run, skill, and schema artifacts
- **THEN** `isomer-cli team-templates validate <template-id>` validates that template without relying on `deepsci-org`-specific role ids

#### Scenario: Missing project-local template artifact is rejected
- **WHEN** a project-local Domain Agent Team Template fixture references a missing manifest, participant contract, role profile, generated skill, harness schema, workspace contract, state contract, or run contract
- **THEN** validation reports an Isomer diagnostic naming the missing artifact path and template ref

#### Scenario: Project-local template boundary leak is rejected
- **WHEN** a project-local Domain Agent Team Template fixture contains a concrete Research Topic, Topic Workspace, Topic Agent Team Profile, Agent Team Instance, mailbox, gateway, credential, launch, or Run truth value instead of an allowed placeholder
- **THEN** validation rejects the template as crossing the template boundary

### Requirement: deepsci-org Completion Evidence
The system SHALL keep `deepsci-org` as the seed Domain Agent Team Template while proving its generated package remains reusable, placeholder-bound, and independent of Topic Workspace state.

#### Scenario: Built-in deepsci-org validates through public CLI
- **WHEN** the Milestone 2 validation suite runs
- **THEN** it validates `deepsci-org` through `isomer-cli team-templates list`, `isomer-cli team-templates inspect deepsci-org`, and `isomer-cli team-templates validate deepsci-org`

#### Scenario: deepsci-org role expectations stay scoped to built-in deepsci-org
- **WHEN** validation inspects the built-in `deepsci-org` template
- **THEN** it enforces the seven expected `deepsci-org` role ids, scalable `experimenter` and `analyzer` metadata, required skills, optional skills, Capability Binding placeholders, and Skill Binding Projection placeholders

#### Scenario: Generic templates are not forced into deepsci role ids
- **WHEN** validation inspects a non-`deepsci-org` project-local Domain Agent Team Template fixture
- **THEN** it validates generic Agent Role, Workflow Stage, artifact, and boundary shape without requiring the seven `deepsci-org` role ids

### Requirement: Template Completion Roadmap Gate
The system SHALL mark Milestone 2 complete only after template registration, validation, CLI, fixture, documentation, and OpenSpec validation gates pass.

#### Scenario: Milestone 2 roadmap items are marked after validation
- **WHEN** template fixture tests, built-in `deepsci-org` tests, `openspec validate --all`, lint, typecheck, unit tests, and research skill validation all pass
- **THEN** the Milestone 2 checklist in `ROADMAP.md` is marked complete

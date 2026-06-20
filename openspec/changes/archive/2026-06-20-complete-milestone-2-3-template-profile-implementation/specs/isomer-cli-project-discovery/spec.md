## ADDED Requirements

### Requirement: Profile Write Output Contract
The system SHALL produce deterministic text and JSON output for Topic Agent Team Profile specialization previews and writes.

#### Scenario: Profile preview reports no written path
- **WHEN** a user runs `isomer-cli team-profiles specialize` without `--write` and requests JSON
- **THEN** the output includes the candidate profile, validation report, and `written_path` as null

#### Scenario: Profile write reports written path
- **WHEN** a user runs `isomer-cli team-profiles specialize --write` and requests JSON
- **THEN** the output includes the candidate profile, validation report, non-null `written_path`, and a deterministic `registration_suggestion` object

#### Scenario: Profile write does not mutate manifest
- **WHEN** `team-profiles specialize --write` writes a profile file
- **THEN** the Project Manifest and Research Topic Config files are unchanged unless a future explicit registration command or flag is added

### Requirement: Fixture Project Validation Commands
The system SHALL validate milestone fixture Projects through the public CLI surfaces used by normal Projects.

#### Scenario: Fixture Project validate command is deterministic
- **WHEN** the validation suite runs `isomer-cli validate --json` against the Milestone 2 and 3 fixture Project
- **THEN** the output has deterministic JSON and reports no diagnostics for the positive fixture

#### Scenario: Fixture template commands are deterministic
- **WHEN** the validation suite runs `team-templates list`, `team-templates inspect`, and `team-templates validate` against fixture Projects
- **THEN** the output has deterministic text and JSON for built-in and project-local template refs

#### Scenario: Fixture profile commands are deterministic
- **WHEN** the validation suite runs `team-profiles specialize` and `team-profiles validate` against fixture Projects
- **THEN** the output has deterministic text and JSON for preview, write, and validation flows

### Requirement: Milestone Documentation Completion
The system SHALL document the completed Milestone 2 and 3 command surface and fixture expectations.

#### Scenario: Developer docs describe template and profile completion
- **WHEN** Milestone 2 and 3 are completed
- **THEN** README or developer notes describe `team-templates`, `team-profiles`, fixture Project expectations, no-launch boundaries, and profile write semantics

#### Scenario: Roadmap reflects verified completion
- **WHEN** all Milestone 2 and 3 verification commands pass
- **THEN** ROADMAP Milestone 2 and 3 checklist items are marked complete without marking Milestone 4 or Houmao launch work complete

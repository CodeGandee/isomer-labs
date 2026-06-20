## ADDED Requirements

### Requirement: Static Use-Case Profile Fixture Projects
The system SHALL provide reusable Project fixture files for UC-01, UC-02, UC-03, and UC-05 Topic Agent Team Profiles before live execution exists.

#### Scenario: Positive use-case fixture Project validates through CLI
- **WHEN** the validation suite loads the use-case fixture Project from repository fixture files
- **THEN** `isomer-cli validate` accepts the Project Manifest, Research Topic Config files, Topic Agent Team Profile registrations, and four use-case profile files

#### Scenario: Each use-case profile fixture validates through profile CLI
- **WHEN** the validation suite runs `isomer-cli team-profiles validate` for UC-01, UC-02, UC-03, and UC-05 profile files
- **THEN** each profile validates without launching agents or creating Workspace Runtime state

#### Scenario: Two topics share deepsci-org without leaking refs
- **WHEN** the use-case fixture Project contains at least two Research Topics that specialize `deepsci-org`
- **THEN** the profiles share Domain Agent Team Template identity while using distinct Research Topic refs, Topic Workspace refs, Agent Workspace refs, policy refs, expected Artifact refs, and profile ids

### Requirement: Topic Profile Specialization Write Contract
The system SHALL keep Topic Agent Team Profile specialization side-effect-light and explicit about file writes and Project registration.

#### Scenario: Profile specialization preview remains side-effect free
- **WHEN** a user runs `isomer-cli team-profiles specialize` without `--write`
- **THEN** the command emits a candidate profile and validation result without writing files, editing the Project Manifest, editing Research Topic Config files, creating Agent Workspaces, or creating Workspace Runtime state

#### Scenario: Profile specialization write creates only profile file
- **WHEN** a user runs `isomer-cli team-profiles specialize --write`
- **THEN** the command writes the Topic Agent Team Profile file under the Project Config Directory and does not implicitly edit the Project Manifest or Research Topic Config files

#### Scenario: Profile specialization write reports registration guidance
- **WHEN** `team-profiles specialize --write` succeeds
- **THEN** text and JSON output report the written path and deterministic registration guidance for adding the profile ref to Project Manifest or Research Topic Config

### Requirement: Topic Profile Negative Validation Completion
The system SHALL reject profile records that would make Milestone 3 depend on runtime, launch, cross-topic, or secret state.

#### Scenario: Duplicate profile ids are rejected regardless of status
- **WHEN** a Project Manifest declares duplicate Topic Agent Team Profile ids
- **THEN** validation rejects the duplicate ids regardless of registration status
- **AND** profile lineage, archive, fork, and migration relationships are left to a future relationship or history record rather than duplicate Project Manifest registrations

#### Scenario: Missing required role binding is rejected
- **WHEN** a Topic Agent Team Profile omits a required Agent Role binding from the source Domain Agent Team Template
- **THEN** profile validation reports the missing role binding without launching agents

#### Scenario: Missing scalable-role fanout is rejected
- **WHEN** a Topic Agent Team Profile activates `deepsci-org-experimenter` or `deepsci-org-analyzer` without a bounded Research Task fanout policy
- **THEN** profile validation rejects the profile before launch preparation

#### Scenario: Automatic mode requires explicit policy ref
- **WHEN** a Topic Agent Team Profile selects automatic execution mode
- **THEN** profile validation requires an automatic-mode policy ref

#### Scenario: Reviewer access policy is required
- **WHEN** a Topic Agent Team Profile activates `deepsci-org-reviewer`
- **THEN** profile validation requires an explicit reviewer read-access policy

#### Scenario: Houmao and launch state are rejected from profile files
- **WHEN** a Topic Agent Team Profile file contains launch dossiers, mailbox state, gateway state, live Houmao managed-agent ids, Agent Team Instance ids, adapter launch facts, command outputs, credentials, tokens, API keys, passwords, or secret material
- **THEN** profile validation rejects the file and reports the offending field without exposing secret values

### Requirement: Profile Completion Roadmap Gate
The system SHALL mark Milestone 3 complete only after use-case fixtures, profile specialization, negative validation, documentation, and OpenSpec validation gates pass.

#### Scenario: Milestone 3 roadmap items are marked after validation
- **WHEN** use-case fixture tests, profile specialization tests, profile negative validation tests, `openspec validate --all`, lint, typecheck, unit tests, and research skill validation all pass
- **THEN** the Milestone 3 checklist in `ROADMAP.md` is marked complete

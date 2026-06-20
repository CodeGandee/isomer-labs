# topic-agent-team-profile-specialization Specification

## Purpose
Define design-time specialization and validation of Topic Agent Team Profiles from registered Domain Agent Team Templates before any Agent Team Instance or Houmao launch state exists.
## Requirements
### Requirement: Topic Agent Team Profile Specialization
The system SHALL derive Topic Agent Team Profiles from registered Domain Agent Team Templates using Effective Topic Context and project-scoped configuration refs.

#### Scenario: Profile specialization consumes topic context
- **WHEN** a user specializes `deepsci-org` for a selected Research Topic
- **THEN** the system uses the selected Project, Research Topic, Research Topic Config, Topic Workspace ref, template ref, policy refs, Capability Binding refs, Skill Binding Projection refs, provider refs, and source metadata from Effective Topic Context

#### Scenario: Profile specialization does not launch agents
- **WHEN** a Topic Agent Team Profile is created or validated
- **THEN** the system does not create Agent Team Instances, Agent Instances, Workspace Runtime records, Run records, mailboxes, gateways, live process ids, or Houmao launch material

#### Scenario: Profile output is project scoped
- **WHEN** the system writes a Topic Agent Team Profile
- **THEN** the profile is stored under a Project Config Directory path referenced by the Project Manifest or Research Topic Config and not under a Topic Workspace `teams/` directory

### Requirement: Placeholder Resolution
The system SHALL resolve template placeholders into topic-specific profile values or report bounded diagnostics before launch preparation.

#### Scenario: Required placeholders are resolved
- **WHEN** a Topic Agent Team Profile is validated
- **THEN** validation confirms that required Research Topic, Topic Workspace, Agent Profile, Capability Binding, Skill Binding Projection, Agent Workspace, Coordination Policy, Gate Policy, Scheduler Policy, provider binding, expected Artifact, and baseline-waiver refs are either resolved or explicitly marked unavailable with a diagnostic

#### Scenario: Unresolved launch placeholders do not block design-time validation
- **WHEN** a profile has no Agent Team Instance id, mailbox refs, gateway refs, live Houmao agent ids, or adapter launch facts
- **THEN** validation treats those launch facts as out of scope for the profile layer rather than as missing profile fields

#### Scenario: Runtime truth is rejected from profiles
- **WHEN** a Topic Agent Team Profile contains Run status, command outputs, live process ids, mailbox state, gateway state, rich Artifact contents, Evidence Items, Findings, Gates, Decision Records, Provenance Records, credentials, tokens, API keys, passwords, or secret material
- **THEN** validation rejects those fields and reports the offending path without exposing secret values

### Requirement: Role Selection and Fanout Validation
The system SHALL validate topic-specific role choices, role constraints, and fanout posture against the source Domain Agent Team Template.

#### Scenario: Required deepsci-org roles remain active unless explicitly unsupported
- **WHEN** a profile specializes the `deepsci-org` template
- **THEN** validation confirms that required roles are active or that the profile records a diagnostic explaining why the profile cannot launch with the current role selection

#### Scenario: Role bindings match selected roles
- **WHEN** a profile activates an Agent Role
- **THEN** validation confirms that the selected Agent Profile ref, Capability Binding ref, Skill Binding Projection ref, Agent Workspace ref, required skill refs, and policy refs match the role slots declared by the source template

#### Scenario: Scalable roles require fanout policy
- **WHEN** a profile enables task-level fanout for `deepsci-org-experimenter` or `deepsci-org-analyzer`
- **THEN** validation requires a bounded fanout policy, distinct Agent Workspace refs for each shard or future shard allocation rule, and a recorded Parallel Execution Scope of Research Task

#### Scenario: Reviewer access policy is explicit
- **WHEN** a profile grants `deepsci-org-reviewer` broad Peer Read Access
- **THEN** validation requires an explicit Coordination Policy or profile constraint documenting that read posture

### Requirement: Multi-Topic Profile Isolation
The system SHALL allow multiple Research Topics to specialize the same Domain Agent Team Template while keeping topic-specific refs isolated.

#### Scenario: Two topics share one template
- **WHEN** one Project defines two Research Topics that both specialize the `deepsci-org` Domain Agent Team Template
- **THEN** validation accepts separate Topic Agent Team Profiles that share template identity but use distinct Research Topic refs, Topic Workspace refs, Agent Workspace refs, policy choices, profile ids, and expected Artifact refs

#### Scenario: Cross-topic profile leakage is rejected
- **WHEN** a Topic Agent Team Profile for one Research Topic references another Research Topic's Topic Workspace, Agent Workspace, default profile id, expected Artifact ref, or topic-local policy ref
- **THEN** validation reports a diagnostic that names both conflicting topic sources

#### Scenario: Duplicate profile ids are rejected
- **WHEN** two Topic Agent Team Profiles in one Project use the same profile id for different Research Topics
- **THEN** validation rejects the duplicate profile id unless the Project Manifest explicitly marks one profile as an archived or historical ref

### Requirement: Use-Case Profile Fixtures
The system SHALL provide static Topic Agent Team Profile fixtures for roadmap use cases before live execution exists.

#### Scenario: UC-01 profile fixture validates
- **WHEN** the UC-01 fixture specializes `deepsci-org` for exploring a new research direction
- **THEN** validation confirms roles, expected Artifacts, follow-up inquiry Gate policy, and profile refs without launching agents

#### Scenario: UC-02 profile fixture validates
- **WHEN** the UC-02 fixture specializes `deepsci-org` for baseline reproduction and optimization
- **THEN** validation confirms Measurable Objective refs, baseline acceptance or waiver policy refs, experiment and analysis role bindings, and expected metric Artifacts

#### Scenario: UC-03 profile fixture validates
- **WHEN** the UC-03 fixture specializes `deepsci-org` for paper revision planning
- **THEN** validation confirms feedback mapping, claim-risk, writer, reviewer, targeted-analysis, and final approval Gate refs

#### Scenario: UC-05 profile fixture validates
- **WHEN** the UC-05 fixture specializes `deepsci-org` for mixed manual and automatic Runs
- **THEN** validation confirms manual-mode defaults, automatic-mode opt-in refs, Completion Watcher Contract refs, Service Request policy refs, and task-level handoff constraints

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


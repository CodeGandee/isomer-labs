## ADDED Requirements

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

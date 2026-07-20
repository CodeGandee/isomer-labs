## ADDED Requirements

### Requirement: Ambient Workspace Location Is Independent from Effective Context
The system SHALL classify the process cwd against registered semantic workspace boundaries without treating Effective Context defaults as evidence of physical location or active acting posture.

#### Scenario: Project root remains Project location
- **WHEN** cwd is the Project root and the Project Manifest defines a default Research Topic or the selected Topic Workspace Manifest has one active Topic Actor
- **THEN** ambient location reports the Project root without claiming that cwd is inside that Research Topic or Topic Actor Workspace
- **AND** Effective Context may separately report its manifest-derived selection and source

#### Scenario: Topic Main is not a worker workspace
- **WHEN** cwd is inside the selected Topic Main Development Repository
- **THEN** ambient location reports Topic Main and its owning Research Topic and Topic Workspace
- **AND** it does not infer Topic Actor or Agent location from a sole manifest actor, Agent Workspace template, or Topic Main ownership

#### Scenario: Worker workspace is identified from registered paths
- **WHEN** canonical cwd is inside exactly one registered Topic Actor Workspace or Agent Workspace
- **THEN** ambient location reports the most specific worker workspace root, worker kind, worker name, owning Research Topic, and source `cwd`

#### Scenario: Ambiguous physical match is rejected
- **WHEN** canonical cwd matches equal-specificity registered workspace roots with incompatible owners
- **THEN** ambient location reports a conflict diagnostic
- **AND** it does not choose an owner from manifest ordering or a default selection

### Requirement: Task Context Alignment Is Explicit and Source-Aware
The system SHALL compare a caller-declared operation scope and target selectors with ambient location and Effective Context while preserving deterministic selector precedence.

#### Scenario: Explicit topic target overrides ambient topic
- **WHEN** a caller checks a topic-scoped operation with explicit `--topic beta` while cwd is at the Project root or inside Research Topic `alpha`
- **THEN** the check selects `beta` according to explicit-selector precedence
- **AND** it reports the ambient difference as an explicit override rather than silently changing the target or blocking the command solely because cwd differs

#### Scenario: Manifest topic default is a fallback only
- **WHEN** a topic-scoped check has no explicit, cwd, environment, or recorded topic selection and uses the Project Manifest default
- **THEN** the check reports the selected Research Topic with source `Project Manifest default`
- **AND** it does not report that default as ambient location or active Topic Actor or Agent posture

#### Scenario: Sole manifest actor is not active posture
- **WHEN** Effective Topic Actor Context resolves from one active Topic Workspace Manifest binding with source `manifest default`
- **THEN** identity output may expose that effective actor candidate for path resolution
- **AND** alignment output reports that no active Topic Actor posture was established solely by that fallback

#### Scenario: Implicit context conflict blocks mutation
- **WHEN** a context-sensitive operation has incompatible implicit topic or worker sources and no explicit selector resolves the conflict
- **THEN** alignment reports a conflict that names the sources
- **AND** the caller does not receive authorization to mutate either target

#### Scenario: Worker posture requires matching resolved worker
- **WHEN** a caller checks a Topic Actor- or Agent-scoped posture with an explicit worker target
- **THEN** alignment reports the resolved worker workspace and whether ambient cwd matches it
- **AND** a switched-workflow caller can treat a mismatch as a cwd-discipline blocker without changing the selected identity

#### Scenario: Alignment check does not persist posture
- **WHEN** any caller checks Project, topic, Topic Actor, or Agent scope
- **THEN** the system returns process-local resolution and alignment evidence
- **AND** it does not write active identity or posture to Project configuration, local context, Topic Workspace configuration, or Workspace Runtime

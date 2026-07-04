## ADDED Requirements

### Requirement: Switch Identity Operator Skill
The system SHALL provide an operator skill named `isomer-op-switch-identity` that lets a Project Operator switch working identity posture to a selected Topic Actor or Agent.

#### Scenario: Skill bundle follows Imsight create structure
- **WHEN** the `isomer-op-switch-identity` skill bundle is inspected
- **THEN** it contains `SKILL.md`
- **AND** it contains `agents/openai.yaml`
- **AND** `SKILL.md` frontmatter name is `isomer-op-switch-identity`
- **AND** the frontmatter description starts with `Use when`
- **AND** the top-level workflow is a concise numbered list with a freeform fallback

#### Scenario: Skill uses command detail pages only where needed
- **WHEN** the skill exposes public routines
- **THEN** it uses the Imsight collection-of-routines subcommand shape
- **AND** it links command detail pages under `commands/`
- **AND** it does not create empty `references/`, `assets/`, or `scripts/` directories for symmetry

### Requirement: Identity Switch Target Resolution
The skill SHALL resolve each switch target through Project Manifest-backed Isomer context and semantic workspace path resolution.

#### Scenario: Topic Actor target resolves actor workspace
- **WHEN** the user asks to switch to a Topic Actor
- **THEN** the skill resolves the selected Project, Research Topic, Topic Workspace, Topic Actor binding, and `topic.actors.workspace`
- **AND** it uses `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>` or equivalent API evidence for the target cwd

#### Scenario: Agent target resolves agent workspace
- **WHEN** the user asks to switch to an Agent
- **THEN** the skill resolves the selected Project, Research Topic, Topic Workspace, Agent Name, and `agent.workspace`
- **AND** it uses `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>` or equivalent API evidence for the target cwd

#### Scenario: Ambiguous target blocks switch
- **WHEN** the user request does not clearly identify one Topic Actor or one Agent target
- **THEN** the skill asks for the target kind and name before switching
- **AND** it does not infer the target by scanning workspace directories

### Requirement: Identity Switch Persistence Modes
The skill SHALL distinguish one-task switches from persistent session switches.

#### Scenario: Act-as executes one prompt and restores identity
- **WHEN** the user invokes `act-as` with a target identity and a following prompt
- **THEN** the skill resolves the target identity, executes only that prompt under the target identity posture, and restores the previous Project Operator identity posture after the task summary
- **AND** it does not leave a persistent switch active unless the user separately requests a persistent switch

#### Scenario: One-task switch reverts after requested work
- **WHEN** the user asks to switch identity for one task or does not request persistence
- **THEN** the skill treats the switched identity as active only for the bounded requested task
- **AND** it reports that normal Project Operator identity is restored after the task summary

#### Scenario: Persistent switch remains active in session memory
- **WHEN** the user asks the switch to persist
- **THEN** the Project Operator remembers the selected identity posture for the current operator session
- **AND** subsequent plans and commands default to that identity's resolved workspace cwd until the user switches again or resets identity

#### Scenario: Reset clears persistent switch
- **WHEN** the user asks to switch back, reset identity, or stop acting as the selected worker
- **THEN** the skill clears the active switched identity posture
- **AND** future commands no longer default to the previous actor or agent workspace cwd

### Requirement: Switched Identity Cwd Discipline
The skill SHALL make the selected actor or agent workspace the default cwd for switched work.

#### Scenario: Commands run from target workspace
- **WHEN** a switched identity is active and the operator runs commands for the requested task
- **THEN** the command cwd is the resolved `topic.actors.workspace` or `agent.workspace`
- **AND** any command that must run elsewhere states the reason and uses a resolved semantic path

#### Scenario: Project root is not the switched cwd
- **WHEN** a switched identity has a resolved workspace
- **THEN** the skill does not use the Project root, Topic Workspace root, or `topic.repos.main` as the default cwd
- **AND** it reports a blocker if the selected actor or agent workspace cannot be resolved or is unsafe

#### Scenario: Working conventions follow target identity
- **WHEN** a switched identity is active
- **THEN** the operator follows the target's workspace conventions, branch posture, output policy, env readiness, handoff expectations, and relevant skill instructions

### Requirement: Switch Identity Provenance
The skill SHALL preserve clear provenance for operator work performed under a switched identity posture.

#### Scenario: Operator does not fabricate worker execution
- **WHEN** the Project Operator completes work under a switched identity posture
- **THEN** the output states that the Project Operator acted as or on behalf of the selected Topic Actor or Agent
- **AND** it does not claim that an independent Topic Actor process, launched Agent Instance, Houmao agent, or Execution Adapter produced the work unless verified runtime evidence exists

#### Scenario: Formal agent claims require formal context
- **WHEN** the switched target is an Agent Name without verified Agent Instance context
- **THEN** durable record guidance may include the Agent Name workspace context
- **AND** it does not include Agent Instance or Agent Team Instance refs as production metadata

#### Scenario: Topic Actor claims use actor metadata
- **WHEN** the switched target is a Topic Actor
- **THEN** durable record guidance uses the selected Topic Actor metadata when accepted record commands require worker metadata
- **AND** it keeps Topic Actor identity distinct from Agent Name and Agent Instance identity

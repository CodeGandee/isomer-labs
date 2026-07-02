## ADDED Requirements

### Requirement: Topic Creator Operator Skill
The repository SHALL provide a command-style operator skill named `isomer-admin-topic-creator` as the canonical user-facing workflow for initializing a Research Topic from empty or partial Project state to manual-research-ready Topic Workspace.

#### Scenario: Topic creator skill bundle exists
- **WHEN** the operator skillset is inspected
- **THEN** it contains `skillset/operator/isomer-admin-topic-creator/SKILL.md` and `skillset/operator/isomer-admin-topic-creator/agents/openai.yaml`
- **AND** the folder name, `SKILL.md` frontmatter `name`, `agents/openai.yaml` display name, and default prompt use `isomer-admin-topic-creator`

#### Scenario: Topic creator is the user-facing topic initialization entrypoint
- **WHEN** a user asks to create, initialize, prepare, or start a Research Topic for manual research from empty or partial Project state
- **THEN** the operator routes to `isomer-admin-topic-creator`
- **AND** the user does not need to know the separate project manager, topic preparation, workspace manager, manual research session, service setup, or research bootstrap skill sequence

### Requirement: Topic Creator Command Surface
The Topic Creator skill SHALL expose a command-style workflow with stage commands that can plan, run, resume, inspect, and repair topic initialization.

#### Scenario: Public commands are listed
- **WHEN** `isomer-admin-topic-creator help` runs or the skill is invoked without a prompt
- **THEN** it lists `help`, `plan`, `create`, `ensure-project`, `define-topic`, `register-topic`, `init-runtime`, `setup-topic-env`, `setup-actors`, `bootstrap-research`, `start-manual-research`, `status`, and `repair`
- **AND** it prints what the skill does, required inputs, command functionalities, outputs, and guardrails

#### Scenario: Create runs the happy path
- **WHEN** the user invokes `create` with a concrete topic statement or registered topic ref
- **THEN** the workflow runs the topic initialization ladder from Project readiness through manual-research handoff where each stage is already satisfied, created, delegated, or reported as blocked
- **AND** it reports the next incomplete stage instead of asking the user to discover another operator skill

#### Scenario: Plan is dry-run
- **WHEN** the user invokes `plan`
- **THEN** the skill resolves the current Project and topic state, reports proposed stage actions, required inputs, expected delegated owners, command shapes, blockers, and next action
- **AND** it does not create or modify Project, Topic Workspace, runtime, repository, actor, bootstrap, or start-pack state

#### Scenario: Status explains progress
- **WHEN** the user invokes `status`
- **THEN** the skill reports which initialization stages are ready, blocked, skipped, or not started
- **AND** it names the next command that can advance the topic toward manual-research readiness

#### Scenario: Repair resumes from blockers
- **WHEN** the user invokes `repair` after a failed or partial topic initialization
- **THEN** the skill uses recorded state and Project Manifest-backed context to resume from the blocked stage
- **AND** it does not rerun already-ready destructive or expensive stages unless the user explicitly asks

### Requirement: Topic Creator Initialization Ladder
The Topic Creator skill SHALL define the ordered readiness ladder for making a Topic Workspace available for manual research.

#### Scenario: Blank state can reach manual-research readiness
- **WHEN** the user asks the Topic Creator to create a topic for manual research from a repository with no initialized Isomer Project
- **THEN** the skill ensures Project initialization, defines topic intent, registers the Research Topic and Topic Workspace, initializes or validates Workspace Runtime, prepares topic environment readiness, validates `topic.repos.main`, sets up selected Topic Actors, runs research bootstrap, and writes manual research start packs
- **AND** it reports each delegated skill or CLI surface used for those stages

#### Scenario: Partial state is reused
- **WHEN** some topic initialization stages already exist
- **THEN** the skill validates and reuses ready Project, topic, runtime, environment, actor, bootstrap, and start-pack evidence
- **AND** it only creates, delegates, or repairs missing or blocked stages

#### Scenario: Manual-research-ready output is explicit
- **WHEN** topic creation completes successfully
- **THEN** Essential Output reports the Project root, Research Topic ref, Topic Workspace ref, `topic.repos.main` readiness, Workspace Runtime status, Topic Actor roster, each selected actor cwd, v2 bootstrap status, start-pack record refs, blockers, and next action
- **AND** Complete Output includes commands run, semantic labels, delegated owner evidence, topic environment setup evidence, actor binding details, placeholder binding entrypoints, storage recording command shapes, and actor-local pointer paths

### Requirement: Topic Creator Delegates Lower-Level Ownership
The Topic Creator skill SHALL orchestrate existing owners rather than duplicating their lower-level mutation responsibilities.

#### Scenario: Project lifecycle remains delegated
- **WHEN** Project initialization, validation, cleanup, content-root relocation, topic listing, or generic Project diagnostics are needed
- **THEN** the Topic Creator delegates or routes that work to `isomer-admin-project-mgr` or supported `isomer-cli project ...` surfaces

#### Scenario: Topic environment remains delegated
- **WHEN** topic environment requirements, topic env target specs, Topic Main Development Repository setup, projection materialization, or topic-root verification are needed
- **THEN** the Topic Creator delegates setup to `isomer-srv-topic-env-setup` through the existing topic environment readiness workflow

#### Scenario: Topic Actor topology remains delegated
- **WHEN** Topic Actor registration, update, archive, materialization, repair, diagnostics, branch validation, or Topic Actor Workspace worktree setup is needed
- **THEN** the Topic Creator delegates that work to `isomer-admin-topic-workspace-mgr` or the backed `project topic-actors ...` CLI surface

#### Scenario: Manual session finalization remains compatible
- **WHEN** research bootstrap or start-pack creation needs the existing compatibility workflow
- **THEN** the Topic Creator may delegate to `isomer-rsch-workspace-mgr-v2` and `isomer-admin-manual-research-session`
- **AND** direct users are still guided to use `isomer-admin-topic-creator` as the front door

#### Scenario: Formal team specialization is separate
- **WHEN** the user asks to adapt or instantiate a Domain Agent Team Template
- **THEN** the Topic Creator hands off to `isomer-admin-topic-team-specialize`
- **AND** it does not treat manual Topic Actor readiness as formal Topic Agent Team Profile material, Agent Workspace readiness, or Agent Team Instance creation

### Requirement: Topic Creator Compatibility Deprecation
The Topic Creator change SHALL keep existing compatibility skills available while marking direct use of replaced user-facing flows as deprecated.

#### Scenario: Topic preparation compatibility skill is marked deprecated
- **WHEN** `skillset/operator/isomer-admin-topic-prepare/SKILL.md` frontmatter is inspected
- **THEN** it includes `deprecated: true`
- **AND** it includes a `deprecation` object with `replaced_by: isomer-admin-topic-creator`, direct-user-invocation scope, and a warning that the skill remains available for compatibility and delegated common-preparation steps

#### Scenario: Manual research session compatibility skill is marked deprecated
- **WHEN** `skillset/operator/isomer-admin-manual-research-session/SKILL.md` frontmatter is inspected
- **THEN** it includes `deprecated: true`
- **AND** it includes a `deprecation` object with `replaced_by: isomer-admin-topic-creator`, direct-user-invocation scope, and a warning that the skill remains available for compatibility and delegated start-pack finalization

#### Scenario: Deprecated compatibility skills still validate
- **WHEN** operator skill validation runs
- **THEN** it accepts deprecated compatibility skills that have valid frontmatter, valid deprecation metadata, valid local references, and clear replacement guidance
- **AND** it does not require the compatibility skill folders to be removed

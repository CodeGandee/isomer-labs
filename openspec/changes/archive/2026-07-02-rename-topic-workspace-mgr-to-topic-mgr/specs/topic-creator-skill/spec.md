## MODIFIED Requirements

### Requirement: Topic Creator Delegates Lower-Level Ownership
The Topic Creator skill SHALL orchestrate existing owners rather than duplicating their lower-level mutation responsibilities.

#### Scenario: Project lifecycle remains delegated
- **WHEN** Project initialization, validation, cleanup, content-root relocation, topic listing, or generic Project diagnostics are needed
- **THEN** the Topic Creator delegates or routes that work to `isomer-admin-project-mgr` or supported `isomer-cli project ...` surfaces

#### Scenario: Topic environment remains delegated
- **WHEN** topic environment requirements, topic env target specs, Topic Main Development Repository setup, projection materialization, or topic-root verification are needed
- **THEN** the Topic Creator delegates setup to `isomer-srv-topic-env-setup` through the existing topic environment readiness workflow

#### Scenario: Initialized topic management remains delegated
- **WHEN** Topic Actor registration, update, archive, materialization, repair, diagnostics, branch validation, Topic Actor Workspace worktree setup, storage inspection, environment package mutation, or environment verification is needed after topic registration
- **THEN** the Topic Creator delegates that work to `isomer-admin-topic-mgr` or the backed CLI and service surfaces selected by that manager

#### Scenario: Topic Creator finalization can consume topic manager evidence
- **WHEN** Topic Creator finalization summarizes initialized-topic readiness
- **THEN** it may consume `isomer-admin-topic-mgr` status, actor, storage, environment, or validation evidence as delegated owner evidence
- **AND** it does not prescribe a next research command or claim research-paradigm v2 bootstrap readiness from topic-manager evidence alone

#### Scenario: Manual session finalization remains compatible
- **WHEN** research bootstrap or start-pack creation needs the existing compatibility workflow
- **THEN** the Topic Creator may delegate to `isomer-rsch-workspace-mgr-v2` and `isomer-admin-manual-research-session`
- **AND** direct users are still guided to use `isomer-admin-topic-creator` as the front door

#### Scenario: Formal team specialization is separate
- **WHEN** the user asks to adapt or instantiate a Domain Agent Team Template
- **THEN** the Topic Creator hands off to `isomer-admin-topic-team-specialize`
- **AND** it does not treat manual Topic Actor readiness as formal Topic Agent Team Profile material, Agent Workspace readiness, or Agent Team Instance creation

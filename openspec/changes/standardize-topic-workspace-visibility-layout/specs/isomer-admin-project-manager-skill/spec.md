## ADDED Requirements

### Requirement: Project Manager Topic Workspace Visibility Guidance
The project manager skill SHALL explain the standard Topic Workspace visibility layout when it initializes, checks, or prepares Workspace Runtime state.

#### Scenario: Runtime guidance reports standard layout
- **WHEN** the user asks the project manager skill to initialize or inspect Workspace Runtime for a Topic Workspace
- **THEN** it explains that `repos/topic-main` and `agents/<agent-name>` are worker-facing Git surfaces, `records/*` is owner-preserved topic record material, and `runtime/` plus `state.sqlite` are runtime-internal surfaces

#### Scenario: Runtime guidance avoids legacy collaboration roots
- **WHEN** project-manager runtime-boundary guidance describes directories created by `isomer-cli project runtime init`
- **THEN** it does not present root `shared/`, `artifacts/`, `tasks/`, `runs/`, `views/`, or `logs/` as normal worker-visible outputs

#### Scenario: Legacy layout is repair guidance
- **WHEN** project-manager diagnostics see legacy root collaboration directories in a Topic Workspace
- **THEN** the skill reports migration guidance and directs repair through explicit operator action instead of telling the user to delete the directories by hand

#### Scenario: Topic workspace manager handoff is named
- **WHEN** the user asks the project manager skill to prepare per-agent worktrees or validate worker visibility boundaries
- **THEN** it hands off to `isomer-admin-topic-workspace-mgr` rather than duplicating Git worktree setup instructions

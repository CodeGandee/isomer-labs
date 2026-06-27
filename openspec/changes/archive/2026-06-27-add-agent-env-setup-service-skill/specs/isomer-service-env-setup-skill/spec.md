## ADDED Requirements

### Requirement: Topic Env Setup Remains Topic Scoped
The Topic Workspace environment setup service SHALL remain responsible for Topic Workspace Pixi dependency readiness and SHALL NOT become the per-agent worktree setup workflow.

#### Scenario: Topic setup does not create agent worktrees
- **WHEN** `isomer-srv-topic-env-setup setup-topic-env` runs
- **THEN** it does not read or create `user-intent/src/agent-env-gate.md`
- **AND** it does not create Agent Workspace Git worktrees, per-agent branches, Agent Workspace boundary material, or `isomer-agent-env-gate.md`

#### Scenario: Topic setup output can be consumed downstream
- **WHEN** topic env setup reports readiness
- **THEN** its output and `user-intent/derived/isomer-env-gate.md` are suitable predecessor evidence for `isomer-srv-agent-env-setup`

#### Scenario: Agent cwd failures route to downstream service
- **WHEN** the Topic Workspace env passes from the Topic Workspace root but a user asks whether it passes from every Agent Workspace cwd
- **THEN** the topic env setup skill routes or points to `isomer-srv-agent-env-setup` instead of claiming per-agent cwd readiness itself

### Requirement: Topic Env Gate Supports Agent-Cwd Consumption
The Topic Workspace environment setup service SHALL keep its derived env gate replayable enough for downstream per-agent cwd verification.

#### Scenario: Derived gate records replayable commands
- **WHEN** `derive-env-gate` writes `user-intent/derived/isomer-env-gate.md`
- **THEN** verification commands use `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...`
- **AND** external runtime wiring is recorded explicitly rather than relying on ambient shell state

#### Scenario: Derived gate distinguishes cwd assumptions
- **WHEN** a verification command must run from the Topic Workspace root or a repo-specific cwd
- **THEN** the derived gate records that cwd assumption so downstream agent env setup can detect agent-cwd incompatibility instead of silently reusing the command

#### Scenario: Topic setup does not claim per-agent Pixi readiness
- **WHEN** topic setup reports `ready`
- **THEN** it claims only the selected Topic Workspace Pixi environment readiness for the topic-level gate
- **AND** it does not claim that every Agent Workspace cwd has passed unless separate `isomer-srv-agent-env-setup` evidence exists

## ADDED Requirements

### Requirement: Agent Env Setup Owns Agent Gate Readiness
The agent environment setup service skill SHALL be the only service skill that reads the source Agent Workspace gate, derives the operational Agent Workspace gate, and claims per-Agent Workspace cwd readiness.

#### Scenario: Agent setup reads source agent gate
- **WHEN** per-Agent Workspace cwd readiness is requested
- **THEN** `isomer-srv-agent-env-setup` reads `user-intent/src/agent-env-gate.md`
- **AND** it treats that file as the source contract for what every authoritative planned Agent Workspace cwd must be able to run

#### Scenario: Agent setup writes derived agent gate
- **WHEN** `isomer-srv-agent-env-setup` derives operational readiness checks
- **THEN** it writes or updates `user-intent/derived/isomer-agent-env-gate.md`
- **AND** it records Agent Names, resolved `agent.workspace` paths, Topic Workspace Pixi binding evidence, verification matrix entries, expected results, blockers, and execution log details

#### Scenario: Overall readiness requires all planned Agent Names
- **WHEN** `isomer-srv-agent-env-setup` reports `overall_readiness_status: ready`
- **THEN** every authoritative planned Agent Name has a valid worktree, required support paths, complete semantic path evidence, and passing verification commands from its resolved `agent.workspace` cwd
- **AND** selected-agent verification remains partial evidence unless the full planned Agent Name matrix has passed

### Requirement: Agent Env Setup Consumes Topic Env as Predecessor Evidence
The agent environment setup service skill SHALL consume Topic Workspace Pixi readiness from topic env setup as predecessor evidence without duplicating topic dependency planning.

#### Scenario: Topic env predecessor is required before agent proof
- **WHEN** `isomer-srv-agent-env-setup` prepares or verifies Agent Workspace cwd readiness
- **THEN** it requires the selected Topic Workspace Pixi binding, `user-intent/derived/isomer-env-gate.md`, and Topic Workspace predecessor readiness evidence before claiming Agent Workspace readiness

#### Scenario: Missing topic dependency readiness routes repair back
- **WHEN** `isomer-srv-agent-env-setup` finds missing, stale, blocked, or failed Topic Workspace dependency readiness
- **THEN** it reports a repair next action naming `isomer-srv-topic-env-setup`
- **AND** it does not mutate Topic Workspace dependencies, create per-agent Pixi manifests, create per-agent lockfiles, or create per-agent `.pixi/` directories by default

#### Scenario: Topic-root pass is not agent readiness
- **WHEN** `isomer-srv-agent-env-setup` reads Topic Workspace predecessor evidence
- **THEN** it treats a topic-root `isomer-env-gate.md` pass as prerequisite evidence only
- **AND** it still verifies the derived agent gate from each required `agent.workspace` cwd before reporting per-agent readiness

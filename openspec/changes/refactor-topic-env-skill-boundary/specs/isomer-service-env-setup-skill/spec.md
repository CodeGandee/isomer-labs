## ADDED Requirements

### Requirement: Topic Env Setup Stops at Topic Workspace Readiness
The service environment setup skill SHALL treat Topic Workspace Pixi readiness as its final readiness boundary and SHALL NOT own Agent Workspace cwd readiness.

#### Scenario: Topic setup reports predecessor evidence
- **WHEN** `isomer-srv-topic-env-setup` completes `setup-topic-env` or `verify-env-gate`
- **THEN** it reports Topic Workspace predecessor evidence including the resolved Topic Workspace, Topic Workspace Pixi binding, source `env-gate.md`, derived `isomer-env-gate.md`, dependency and enclosure records, topic-root verification status, commands run, changed files, blockers, and next action
- **AND** it does not report `overall_readiness_status`, `readiness_by_agent`, Agent Names, Agent Workspace paths, or `isomer-agent-env-gate.md` evidence

#### Scenario: Agent gate files are outside topic setup
- **WHEN** `isomer-srv-topic-env-setup` is invoked for Topic Workspace setup or verification
- **THEN** it does not read `user-intent/src/agent-env-gate.md`
- **AND** it does not create or update `user-intent/derived/isomer-agent-env-gate.md`
- **AND** it does not verify commands from any resolved `agent.workspace` cwd

#### Scenario: Per-agent readiness is a follow-up, not a topic setup call
- **WHEN** topic setup output needs to mention per-Agent Workspace readiness
- **THEN** it states that per-agent readiness is not checked by `isomer-srv-topic-env-setup`
- **AND** it may name `isomer-srv-agent-env-setup` as an operator follow-up only when the caller requested per-agent proof or launch-facing Agent Workspace readiness
- **AND** it does not present the follow-up as a topic env setup subcommand, delegated call, or readiness dependency

### Requirement: Topic Env Call Graph Does Not Show Downstream Agent Readiness Ownership
The service environment setup skill SHALL be represented in skill call graphs as producing Topic Workspace predecessor evidence, not as calling Agent Workspace readiness setup.

#### Scenario: Topic env to agent env edge is absent
- **WHEN** `skillset/callgraph.md` documents top-level skill-to-skill call paths
- **THEN** it does not include a normal call path from `isomer-srv-topic-env-setup` to `isomer-srv-agent-env-setup`
- **AND** any note about per-agent readiness describes it as a caller or operator decision outside topic env setup

#### Scenario: Repair edge remains agent-owned
- **WHEN** the call graph includes the relationship between `isomer-srv-agent-env-setup` and `isomer-srv-topic-env-setup`
- **THEN** it represents the repair route as `isomer-srv-agent-env-setup` requiring or routing missing or stale Topic Workspace environment predecessor evidence back to `isomer-srv-topic-env-setup`

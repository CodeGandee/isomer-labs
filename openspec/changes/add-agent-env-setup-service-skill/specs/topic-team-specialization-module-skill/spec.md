## ADDED Requirements

### Requirement: Topic Team Specialization Uses Agent Env Service Evidence
The Topic Team Specialization module skill SHALL consume `isomer-srv-agent-env-setup` output as durable static setup evidence when Agent Workspace environment readiness is in scope.

#### Scenario: Setup agent workspace delegates env readiness
- **WHEN** `setup-agent-workspace` determines that a specialized topic team needs Git-backed Agent Workspaces and per-agent cwd env verification
- **THEN** it delegates that concrete setup to `isomer-srv-agent-env-setup setup-agent-env` or records an explicit blocker explaining why service delegation cannot run

#### Scenario: Setup records service evidence
- **WHEN** agent env setup service output is available
- **THEN** `setup-agent-workspace` records semantic paths, Agent Names, branch plans, worktree status by agent, source agent env gate path, derived agent env gate path, readiness by agent, commands run, blockers, and next actions as static setup evidence

#### Scenario: Service evidence can satisfy static readiness
- **WHEN** service output reports overall Agent Workspace env readiness as `ready`
- **THEN** `validate-topic-team` may treat Agent Workspace setup and agent-cwd environment posture as ready for static material validation
- **AND** it still does not claim runtime launch readiness

#### Scenario: Missing service evidence blocks readiness when required
- **WHEN** the specialized team requires Agent Workspace env readiness and no service output or explicit deferral exists
- **THEN** `validate-topic-team` reports an Agent Workspace environment setup blocker

### Requirement: Final Topic Summary Reports Agent Env Matrix
The Topic Team Specialization module skill SHALL include service-produced agent environment evidence in final topic summaries.

#### Scenario: Final summary includes gate path
- **WHEN** `finalize-topic-team` writes or updates `isomer-topic-summary.md`
- **THEN** the Agent Workspace layout or environment section includes `user-intent/src/agent-env-gate.md` and `user-intent/derived/isomer-agent-env-gate.md` when those files exist

#### Scenario: Final summary reports per-agent readiness
- **WHEN** service output contains readiness by agent
- **THEN** the final summary lists each Agent Name, resolved `agent.workspace`, branch, env readiness status, and blocker when present

#### Scenario: Runtime boundary remains explicit
- **WHEN** the final summary includes ready Agent Workspace env setup
- **THEN** it states that Agent Team Instance creation, Workspace Runtime records, Houmao launch, and Execution Adapter readiness remain separate downstream steps

## Why

Topic Workspace environment setup currently proves that one operator or agent can run the requested target from the selected Topic Workspace, but live topic teams need a stronger static readiness check: every planned Agent Workspace must exist as a Git worktree and must pass an agent-cwd gate when used as that agent's cwd.

This change adds a bounded service skill for Agent Workspace environment setup so the operator-facing workspace manager can delegate concrete per-agent repo, worktree, support-path, and cwd-based agent-env-gate verification work without creating Agent Instances or launching agents.

## What Changes

- Add a new `skillset/service/isomer-srv-agent-env-setup` command-style service skill.
- Define the service as downstream of `isomer-srv-topic-env-setup`: it consumes Topic Workspace Pixi readiness and `user-intent/derived/isomer-env-gate.md`, but it does not create per-agent Pixi environments.
- Require a user-authored source gate at `user-intent/src/agent-env-gate.md`, beside `user-intent/src/env-gate.md`, to describe the required Agent Workspace cwd commands and success criteria.
- Generate the operational per-agent verification gate at `user-intent/derived/isomer-agent-env-gate.md`, recording the source agent gate, topic env gate, planned agents, resolved semantic paths, Topic Main Repository configuration, worktree status, cwd-based verification commands, expected results, blockers, and execution log.
- Create or reuse the single shared `topic.main_repo` normal repository, configure it to satisfy the derived agent env gate within service-safe boundaries, and create per-agent `agent.workspace` Git worktrees using semantic labels and `isomer-default.v1` only as the default binding profile.
- Verify agent environment readiness from each resolved Agent Workspace cwd by running every required command from the derived agent env gate through recorded `pixi run --manifest-path <manifest_path> --environment <pixi_environment> ...` commands.
- Keep the workflow service-safe: no Agent Instance creation, Workspace Runtime mutation, Houmao launch, Execution Adapter launch, dependency installation by default, destructive Git repair, or research decision authority.
- Update operator skill contracts so Topic Team Specialization and Topic Workspace management can route agent cwd readiness work to the new service and record its evidence.

## Capabilities

### New Capabilities
- `isomer-agent-env-setup-service-skill`: Defines the new service skill that prepares per-agent Git worktrees and verifies the Topic Workspace environment from each Agent Workspace cwd.

### Modified Capabilities
- `topic-workspace-manager-skill`: Routes concrete service-safe Agent Workspace env setup and per-agent cwd gate verification through `isomer-srv-agent-env-setup` when environment readiness is in scope.
- `topic-team-specialization-module-skill`: Treats the new service output as durable static setup evidence for `setup-agent-workspace`, `validate-topic-team`, and final summaries.
- `isomer-service-env-setup-skill`: Clarifies that topic env setup remains topic-scoped and that downstream agent env setup consumes the derived topic env gate rather than creating per-agent Pixi environments.

## Impact

- Adds a service skill bundle under `skillset/service/isomer-srv-agent-env-setup/`, including reference pages and agent UI metadata.
- Adds or updates skillset validation so the service skill requires semantic path evidence, topic env readiness evidence, per-agent worktree verification, and agent-cwd env-gate reporting.
- Updates operator skill guidance in `isomer-admin-topic-workspace-mgr` and `isomer-admin-topic-team-specialize` to delegate or consume the new service evidence.
- May add unit validation fixtures for the service skill and OpenSpec validation coverage.

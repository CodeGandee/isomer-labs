## Why

`isomer-srv-topic-env-setup` has grown from a Topic Workspace Pixi setup skill into a broad environment coordinator that mentions downstream per-agent readiness, package-source policy, NVIDIA policy, repo acquisition, dependency installation, and readiness routing. This blurs the boundary with `isomer-srv-agent-env-setup`, `isomer-srv-resolve-pkg-repo`, `isomer-misc-nvidia-tools`, and operator orchestration, making it too easy for topic-scoped setup to appear responsible for `agent-env-gate.md` or per-Agent Workspace cwd proof.

## What Changes

- Narrow `isomer-srv-topic-env-setup` so its contract ends at Topic Workspace predecessor readiness: `env-gate.md`, `isomer-env-gate.md`, selected Topic Workspace Pixi binding, dependency/enclosure evidence, and topic-root verification.
- Remove or reword topic-env setup instructions that imply it calls, triggers, or reasons over `isomer-srv-agent-env-setup`; topic env setup may report that per-agent readiness is not checked and name the appropriate next action.
- Preserve `isomer-srv-agent-env-setup` as the only skill that reads `agent-env-gate.md`, writes `isomer-agent-env-gate.md`, prepares per-agent worktrees for environment proof, and verifies commands from each resolved `agent.workspace` cwd.
- Route package repository and channel selection through `isomer-srv-resolve-pkg-repo` when reachability, mirrors, registries, or NVIDIA channel choice require explicit resolution.
- Route CUDA/NVIDIA build preferences through `isomer-misc-nvidia-tools` instead of embedding broad NVIDIA decision logic in topic env setup.
- Update operator and call graph documentation so `isomer-admin-topic-team-specialize` owns the decision to invoke topic env setup versus agent env setup, and `isomer-admin-topic-workspace-mgr` remains the Git topology owner.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `isomer-service-env-setup-skill`: Narrow Topic Workspace setup requirements so the skill produces predecessor evidence and does not own per-agent readiness routing or downstream agent gate interpretation.
- `isomer-agent-env-setup-service-skill`: Clarify that Agent Workspace setup consumes topic env predecessor evidence and is the sole owner of `agent-env-gate.md`, `isomer-agent-env-gate.md`, and per-agent cwd verification.
- `isomer-service-env-setup-enclosure`: Keep enclosure policy scoped to Topic Workspace setup while routing package repository/channel selection to the package repository resolver where needed.
- `topic-team-specialization-module-skill`: Clarify operator orchestration between `setup-topic-env`, `setup-agent-workspace`, workspace manager delegation, and agent env setup.

## Impact

- Affected skill docs: `skillset/service/isomer-srv-topic-env-setup/`, `skillset/service/isomer-srv-agent-env-setup/`, `skillset/service/isomer-srv-resolve-pkg-repo/`, `skillset/misc/isomer-misc-nvidia-tools/`, `skillset/operator/isomer-admin-topic-team-specialize/`, and `skillset/operator/isomer-admin-topic-workspace-mgr/`.
- Affected documentation: `skillset/service/README.md`, `skillset/operator/README.md`, and `skillset/callgraph.md`.
- Affected OpenSpec specs: service env setup, agent env setup, env enclosure, and topic team specialization module skill.
- No runtime data migration or public Python API change is expected; this is a skill contract and documentation refactor.

# Status

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the selected Project, Research Topic, Topic Workspace, and semantic path evidence through `storage-resolve`.
2. Inspect initialized-topic storage with `storage-inspect-main` and `storage-validate` in read-only mode when Topic Manager evidence is available.
3. Inspect current Topic Actor bindings and Topic Actor Workspace posture with `actors-diagnose` when actor evidence exists or the user asks about actors.
4. Inspect topic agent team topology with `team-plan` or `team-validate-workspaces` in read-only mode when role binding, packet/profile, Agent Name, or `agent.workspace` evidence exists.
5. Inspect environment evidence without mutation: package mutation records when available, Topic Workspace env setup evidence, actor cwd gate evidence, and agent env service evidence.
6. Inspect reset checkpoint posture with `reset-inspect` in read-only mode when a checkpoint, reset plan, reset outcome, restart, or reset question is in scope.
7. Report initialized-topic readiness, skipped surfaces, blockers, and the next operator action. Use Essential Output by default and Complete Output when requested.

If the user's task does not map cleanly to these steps, report the selected initialized-topic surfaces that can be resolved safely, skip missing optional surfaces, and route missing initialization to `isomer-op-topic-creator`.

## Status Boundary

`status` is read-only unless the user explicitly asks for a follow-up command that mutates storage, actors, team topology, packages, verification evidence, or reset state. It does not create topic-main in the normal flow, create Agent Instances, launch Houmao agents, run Execution Adapters, apply reset plans, or prove every Agent Workspace cwd can run a gate command. Per-Agent Workspace cwd readiness belongs to `isomer-srv-agent-env-setup`.

When the operator asks to add another non-main topic repository, use `storage-register-repo`. Helper-created repositories default under `repos/extern/<repo-label-path>` and are supporting topic-local repositories, not Agent Workspace worktree sources.

Runtime Agent Team Instance creation later consumes validated `agent_name`, branch, `agent.workspace` path plans, and `agent.*` support path plans. Missing semantic label evidence is a launch-facing blocker; runtime must not silently fall back to `<topic-workspace>/agents/<agent-instance-id>`.

## Output

Report `status`, `topic`, `semantic_paths`, `topic_main`, `topic_actors`, `agent_workspaces`, `environment`, `reset_checkpoint`, `tmp_posture`, `changed_paths` when known, blockers, and `next_action`.

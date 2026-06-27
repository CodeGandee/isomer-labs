# Setup Agent Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the specialized topic-team shape, expected Agent Roles, draft profile inputs, registration evidence, registered Topic Workspace path, and topic environment status.
3. Determine whether the requested Agent Workspace layout needs Git-backed `topic.main_repo`, `agent.workspace`, and worker support labels from the selected Topic Workspace Manifest or `isomer-default.v1`.
4. If Git-backed worktrees, `agent.*` worker-facing support paths, peer-readable large artifact paths, generated links, or launch-facing worker Agent Workspaces are needed, delegate the concrete setup to `isomer-admin-topic-workspace-mgr topic-workspace` or the needed subcommand and record its semantic labels, paths, sources, agent names, branches, `isomer-managed/` regime status, generated links, derived compatibility refs, boundary, validation, blocker, and next-action output as durable setup evidence.
5. If the user requested `agent-env-gate.md`, per-Agent Workspace cwd verification, agent environment readiness, or selected-agent repair, delegate the gate-driven setup to `isomer-srv-agent-env-setup setup-agent-env` or the needed subcommand after topic env readiness and Git topology evidence exist. Record `source_agent_env_gate_path`, `agent_env_gate_path`, Topic Main Repository path, Agent Names, resolved `agent.workspace` paths, branch plan, worktree status by agent, readiness by agent, overall readiness, commands run, changed files, blockers, and next action as service evidence.
6. Treat non-Git static setup as an explicit blocker or exception for launch-facing worker Agent Workspaces; if the user intentionally requests non-Git support material, record why it is outside the standard worker layout.
7. Create or report Agent Workspace directories only after the specialized team shape is clear and the target paths are safe.
8. Record agent names, resolved `agent.workspace` paths, required `agent.*` support paths, path sources, role ownership, worker visibility boundary notes, generated-link notes, delegated workspace manager evidence, delegated `isomer-srv-agent-env-setup` evidence, skipped actions, blockers, and validation refs as durable setup material.
9. Report `agent_names`, `agent_workspace_paths`, `semantic_paths`, `isomer_managed_path_status`, `branch_plan`, `topic_main_repo`, `records_root`, delegated derived `agent_workspace_ref` evidence when present, `source_agent_env_gate_path`, `agent_env_gate_path`, `agent_environment_service_output`, readiness by agent, generated links, unresolved workspace blockers, and whether `validate-topic-team` can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step Agent Workspace setup plan from the specialized team shape, Topic Workspace boundary, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- Specialized topic-team shape and draft profile or packet/profile input summary from `specialize-team`.
- Registration assurance from `ensure-topic-registration`, including Project Manifest-backed Research Topic and Topic Workspace refs or an explicit registration blocker.
- `topic_environment_status` or explicit environment setup blocker from `setup-topic-env`.

If the topic environment setup status is missing, refuse to run, explain that Agent Workspace setup depends on the topic environment posture, and tell the user to run `setup-topic-env` first.

If registration evidence is missing or only names a provisional topic workspace seed, refuse to run, explain that Agent Workspace setup needs authoritative Topic Workspace refs, and tell the user to run `ensure-topic-registration` first.

## Guardrails

Use **Topic Workspace** for the topic-level work area and **Agent Workspace** for per-agent work areas.

Do not create Agent Workspaces before team specialization defines expected Agent Roles.

Do not hand-roll Git worktree or `isomer-managed/` setup inside this subcommand. Use `isomer-admin-topic-workspace-mgr` for `repos/topic-main`, `isomer-managed/`, `topic-owner/main`, `per-agent/<agent-name>/main`, derived compatibility refs, generated links, and Git topology validation.

Do not hand-roll per-Agent Workspace environment verification inside this subcommand. Use `isomer-srv-agent-env-setup` for `user-intent/src/agent-env-gate.md`, `user-intent/derived/isomer-agent-env-gate.md`, Topic Main Repository environment configuration, per-agent cwd verification, selected-agent partial evidence, and no-runtime-mutation guardrails.

Do not accept stale workspace setup evidence that names legacy support roots, top-level Topic Main Repository collaboration directories, or default-looking directories without semantic labels and path sources as current readiness. Ask for delegated `isomer-admin-topic-workspace-mgr` validation of semantic labels and the `isomer-managed/` layout instead.

Do not create Agent Instances, start processes, register Workspace Runtime state, or launch agents from this subcommand.

Do not use Agent Workspace setup as a substitute for later runtime registration when runtime records are required by a different workflow.

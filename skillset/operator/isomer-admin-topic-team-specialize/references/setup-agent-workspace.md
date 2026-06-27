# Setup Agent Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the specialized topic-team shape, expected Agent Roles, draft profile inputs, registration evidence, registered Topic Workspace path, topic environment status, `env_gate_path`, `derived_gate_path`, and the user task or requested Agent Workspace cwd readiness target.
3. Determine whether the requested Agent Workspace layout needs Git-backed `topic.repos.main`, `agent.workspace`, and worker support labels from the selected Topic Workspace Manifest or `isomer-default.v1`.
4. If Git-backed worktrees, `agent.*` worker-facing support paths, `topic.repos.main.tmp`, `agent.tmp`, peer-readable large artifact paths, generated links, or launch-facing worker Agent Workspaces are needed, delegate the concrete setup to `isomer-admin-topic-workspace-mgr topic-workspace` or the needed subcommand and record its semantic labels, paths, sources, agent names, branches, `isomer-managed/` regime status, local tmp ignore posture, generated links, derived compatibility refs, boundary, validation, blocker, and next-action output as durable setup evidence.
5. If the user requested `agent-env-gate.md`, per-Agent Workspace cwd verification, agent environment readiness, selected-agent repair, or launch-facing Agent Workspace readiness, ensure the source gate exists at `<topic-workspace>/user-intent/src/agent-env-gate.md`. If it exists, use it as the handoff contract. If it is missing and the task gives a clear per-agent cwd readiness target, create or update a concise `agent-env-gate.md` from the task before service delegation. If the target is unclear, ask the user what every planned Agent Workspace cwd must be able to run and stop before service delegation.
6. Delegate gate-driven Agent Workspace environment setup to `$isomer-srv-agent-env-setup setup-agent-env <research_topic_id>` or the needed direct subcommand only after topic env readiness, `user-intent/derived/isomer-env-gate.md`, source `agent-env-gate.md`, authoritative Agent Names, and Git topology evidence exist. Record `source_agent_env_gate_path`, `agent_env_gate_path`, Topic Main Repository path, Agent Names, resolved `agent.workspace` paths, branch plan, worktree status by agent, readiness by agent, overall readiness, commands run, changed files, blockers, and next action as service evidence.
7. Treat non-Git static setup as an explicit blocker or exception for launch-facing worker Agent Workspaces; if the user intentionally requests non-Git support material, record why it is outside the standard worker layout.
8. Create or report Agent Workspace directories only after the specialized team shape is clear and the target paths are safe.
9. Record agent names, resolved `agent.workspace` paths, required `agent.*` support paths, `topic.repos.main.tmp` and `agent.tmp` posture, path sources, role ownership, worker visibility boundary notes, generated-link notes, delegated workspace manager evidence, delegated `isomer-srv-agent-env-setup` evidence, skipped actions, blockers, and validation refs as durable setup material.
10. Report `agent_names`, `agent_workspace_paths`, `semantic_paths`, `local_tmp_path_status`, `isomer_managed_path_status`, `branch_plan`, `topic_main_repo`, `records_root`, delegated derived `agent_workspace_ref` evidence when present, `source_agent_env_gate_path`, `agent_env_gate_path`, `agent_environment_service_output`, readiness by agent, generated links, unresolved workspace blockers, and whether `validate-topic-team` can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step Agent Workspace setup plan from the specialized team shape, Topic Workspace boundary, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- Specialized topic-team shape and draft profile or packet/profile input summary from `specialize-team`.
- Registration assurance from `ensure-topic-registration`, including Project Manifest-backed Research Topic and Topic Workspace refs or an explicit registration blocker.
- `topic_environment_status` or explicit environment setup blocker from `setup-topic-env`.
- `user-intent/derived/isomer-env-gate.md` and service readiness evidence from `isomer-srv-topic-env-setup` before per-Agent Workspace cwd verification or selected-agent repair.
- A usable `<topic-workspace>/user-intent/src/agent-env-gate.md`, or a clear per-agent cwd readiness target from the task, topic-team material, or user prompt that can be written to that source gate.

If the topic environment setup status is missing, refuse to run, explain that Agent Workspace setup depends on the topic environment posture, and tell the user to run `setup-topic-env` first.

If registration evidence is missing or only names a provisional topic workspace seed, refuse to run, explain that Agent Workspace setup needs authoritative Topic Workspace refs, and tell the user to run `ensure-topic-registration` first.

If per-Agent Workspace cwd verification or selected-agent repair is requested and the source agent env gate is missing, write `<topic-workspace>/user-intent/src/agent-env-gate.md` only when the task clearly states commands, expected results, success criteria, and cwd assumptions for planned Agent Workspaces. If the task is too vague, ask the user for those readiness requirements and stop before calling `isomer-srv-agent-env-setup`.

## Agent Env Gate Handoff

`agent-env-gate.md` is the operator-owned source contract for `isomer-srv-agent-env-setup`. It should describe what every authoritative planned Agent Workspace cwd must be able to do after setup. When the user did not create it, generate it from the task only if the task supplies enough concrete setup intent. Use `<topic-workspace>/user-intent/src/agent-env-gate.md`, create the parent directory when safe, and keep it concise.

Use this source-gate structure when generating the file:

```markdown
# Agent Environment Gate

## Source Task

## Agent Scope

## Topic Env Predecessor

## Required Cwd Commands

## Expected Results

## Topic Main Repository Requirements

## Cwd Assumptions

## Out-of-Scope Requests

## Open Questions
```

`## Source Task` should quote or summarize the user-provided task that caused this gate. `## Agent Scope` should name all planned Agent Names, or state that the authoritative Agent Names must come from the Topic Team Instantiation Packet or Topic Agent Team Profile material. `## Required Cwd Commands` should list concrete commands or state the exact blocker if the task did not give them. `## Expected Results` should say what counts as success. `## Topic Main Repository Requirements` should record non-destructive configuration expectations for `topic.repos.main`. `## Cwd Assumptions` should state whether commands must run from every `agent.workspace` cwd or a selected-agent partial scope. `## Out-of-Scope Requests` should preserve any request for live Agent Instances, Workspace Runtime mutation, Houmao launch, Execution Adapter launch, privileged host mutation, dependency mutation, or research decisions as blockers for the service skill. `## Open Questions` should contain `None.` only when the task is precise enough for service delegation.

Do not generate `user-intent/derived/isomer-agent-env-gate.md` from this operator subcommand. That derived gate belongs to `isomer-srv-agent-env-setup`.

## Service Delegation

Use `isomer-srv-agent-env-setup` for gate-driven Agent Workspace environment readiness after source gate preparation and Git topology evidence:

```text
$isomer-srv-agent-env-setup setup-agent-env <research_topic_id>
$isomer-srv-agent-env-setup verify-agent-env-gate <research_topic_id> --agent <agent-name>
```

Use the full `setup-agent-env` flow for overall readiness. Use direct selected-agent verification only when the user explicitly asks for partial selected-agent repair or rerun evidence.

## Guardrails

Use **Topic Workspace** for the topic-level work area and **Agent Workspace** for per-agent work areas.

Do not create Agent Workspaces before team specialization defines expected Agent Roles.

Do not hand-roll Git worktree or `isomer-managed/` setup inside this subcommand. Use `isomer-admin-topic-workspace-mgr` for `repos/topic-main`, `isomer-managed/`, `topic-owner/main`, `per-agent/<agent-name>/main`, derived compatibility refs, generated links, and Git topology validation.

Do not hand-roll per-Agent Workspace environment verification inside this subcommand. Use `isomer-srv-agent-env-setup` for source gate reading, `user-intent/derived/isomer-agent-env-gate.md`, Topic Main Repository environment configuration, per-agent cwd verification, selected-agent partial evidence, and no-runtime-mutation guardrails.

Do not call `isomer-srv-agent-env-setup` before `user-intent/src/agent-env-gate.md` exists. Generate that source gate from the task only when commands, expected results, and cwd assumptions are clear enough for the service to derive a per-agent verification matrix.

Do not accept stale workspace setup evidence that names legacy support roots, top-level Topic Main Repository collaboration directories, or default-looking directories without semantic labels and path sources as current readiness. Ask for delegated `isomer-admin-topic-workspace-mgr` validation of semantic labels and the `isomer-managed/` layout instead.

Do not accept tmp contents as readiness evidence. `topic.repos.main.tmp` and `agent.tmp` evidence is limited to resolved paths, ignored local disposable posture, and tracked-content diagnostics.

Do not create Agent Instances, start processes, register Workspace Runtime state, or launch agents from this subcommand.

Do not use Agent Workspace setup as a substitute for later runtime registration when runtime records are required by a different workflow.

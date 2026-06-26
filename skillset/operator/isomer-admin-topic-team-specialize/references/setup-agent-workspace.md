# Setup Agent Workspace

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the specialized topic-team shape, expected Agent Roles, draft profile inputs, registration evidence, registered Topic Workspace path, and topic environment status.
3. Determine whether the requested Agent Workspace layout is plain static directories or the Git-backed layout with `<topic-workspace-dir>/repos/topic-main` and per-agent worktrees.
4. If Git-backed worktrees are requested, delegate the concrete setup to `isomer-admin-topic-workspace-mgr topic-workspace` or the needed subcommand and record its `agent_workspace_ref`, branch, boundary, validation, blocker, and next-action output as durable setup evidence.
5. For non-Git static setup, determine per-agent Agent Workspace directories, ownership notes, allowed file surfaces, and boundary notes needed for the expected Agent Roles.
6. Create or report Agent Workspace directories only after the specialized team shape is clear and the target paths are safe.
7. Record workspace paths, role ownership, boundary notes, delegated workspace manager evidence, skipped actions, blockers, and validation refs as durable setup material.
8. Report `agent_workspace_paths`, delegated `agent_workspace_ref` evidence, unresolved workspace blockers, and whether `validate-topic-team` can proceed.

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

Do not hand-roll Git worktree setup inside this subcommand. Use `isomer-admin-topic-workspace-mgr` for `repos/topic-main`, `per-agent/<agent-key>/main`, `agent_workspace_ref`, and Git topology validation.

Do not create Agent Instances, start processes, register Workspace Runtime state, or launch agents from this subcommand.

Do not use Agent Workspace setup as a substitute for later runtime registration when runtime records are required by a different workflow.

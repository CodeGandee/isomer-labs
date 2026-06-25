# Validate Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read topic definition material, specialization outputs, topic environment setup evidence, Agent Workspace paths, delegated Git-backed workspace manager evidence, deferrals, blockers, and validation refs.
3. Check that `topic-overview.md` exists and reflects the current Research Topic understanding.
4. Check that copied specialization material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, and draft profile inputs exist or have explicit blockers.
5. Check that topic environment setup and Agent Workspace setup are ready as durable preparation, intentionally deferred, or blocked with named next actions. When Git-backed worktrees were requested, require `isomer-admin-topic-workspace-mgr` validation evidence or report missing delegated setup as a blocker.
6. Report `topic_team_validation_status` as ready, ready-with-deferrals, blocked, or not checked for static material readiness, and name the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static-material validation plan from the available topic-team artifacts, setup outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- `<topic-dir>/topic-def/topic-overview.md`.
- Specialized topic-team material and draft profile or packet/profile input summary from `specialize-team`.
- `topic_environment_status` or explicit setup blocker from `setup-topic-env`.
- `agent_workspace_paths` or explicit workspace blocker from `setup-agent-workspace`.

If environment status or Agent Workspace paths are missing, refuse to run, explain that readiness validation depends on setup outputs, and tell the user to run `setup-topic-env` and `setup-agent-workspace` first. If the requested Agent Workspace layout is Git-backed and delegated workspace manager evidence is missing, report that missing delegated setup as a blocker.

## Guardrails

Do not claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from this validation.

Do not treat deferrals as harmless. Mark whether each deferral blocks static setup, validation, profile materialization, or later runtime operation.

Do not run materialization or live operation from validation.

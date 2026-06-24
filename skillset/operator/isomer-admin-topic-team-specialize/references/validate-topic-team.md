# Validate Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read topic definition material, specialization outputs, topic environment status, Agent Workspace paths, deferrals, blockers, and validation refs.
3. Check that `topic-overview.md` exists and reflects the current Research Topic understanding.
4. Check that copied specialization material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, and draft profile inputs exist or have explicit blockers.
5. Check that topic environment setup and Agent Workspace setup are ready, intentionally deferred, or blocked with named next actions.
6. Report `topic_team_validation_status` as ready, ready-with-deferrals, blocked, or not checked, and name the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step readiness validation plan from the available topic-team artifacts, setup outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts:

- `<topic-dir>/topic-def/topic-overview.md`.
- Specialized topic-team material and draft profile or packet/profile input summary from `specialize-team`.
- `topic_environment_status` or explicit setup blocker from `setup-topic-env`.
- `agent_workspace_paths` or explicit workspace blocker from `setup-agent-workspace`.

If environment status or Agent Workspace paths are missing, refuse to run, explain that readiness validation depends on setup outputs, and tell the user to run `setup-topic-env` and `setup-agent-workspace` first.

## Guardrails

Do not claim the team can start when required topic overview, specialization, environment, workspace, approval, runtime, or adapter evidence is missing.

Do not treat deferrals as harmless. Mark whether each deferral blocks launch, setup, validation, or later research execution.

Do not run launch or materialization work from validation.

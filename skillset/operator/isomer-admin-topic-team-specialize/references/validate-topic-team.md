# Validate Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read topic definition material, specialization outputs, topic environment status, Agent Workspace paths, deferrals, blockers, and validation refs.
2. Check that `topic-overview.md` exists and reflects the current Research Topic understanding.
3. Check that copied specialization material, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, and draft profile inputs exist or have explicit blockers.
4. Check that topic environment setup and Agent Workspace setup are ready, intentionally deferred, or blocked with named next actions.
5. Report `topic_team_validation_status` as ready, ready-with-deferrals, blocked, or not checked, and name the next safe subcommand.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step readiness validation plan from the available topic-team artifacts, setup outputs, and guardrails, then execute the plan.

## Guardrails

Do not claim the team can start when required topic overview, specialization, environment, workspace, approval, runtime, or adapter evidence is missing.

Do not treat deferrals as harmless. Mark whether each deferral blocks launch, setup, validation, or later research execution.

Do not run launch or materialization work from validation.

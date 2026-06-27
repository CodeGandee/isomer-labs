# Finalize Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the topic overview, registration assurance evidence, specialization outputs, durable setup records including `isomer-srv-topic-env-setup` evidence, Agent Workspace records, agent names, branch plans, delegated Git-backed workspace manager evidence, validation status, blockers, deferrals, and next action refs.
3. Create or update `isomer-topic-summary.md` in the registered Topic Workspace root, or stop with an explicit registration blocker when only a provisional topic workspace seed exists.
4. Include the sections in **Summary Template** and keep blockers visible when validation is incomplete, including registration blockers, missing Topic Workspace Pixi binding evidence, and missing delegated `isomer-admin-topic-workspace-mgr` evidence when Git-backed Agent Workspace worktrees were requested.
5. Report `isomer_topic_summary_path`, `topic_team_validation_status`, blockers, deferrals, and next operator action.
6. Stop at the final summary boundary unless the user explicitly asks for `approve-profile` or `materialize-profile`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static finalization plan from the topic-team artifacts, setup records, validation outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifact:

- `topic_team_validation_status` from `validate-topic-team`, including ready, ready-with-deferrals, or blocked status.
- Registration assurance from `ensure-topic-registration`, carried through validation.

If validation status is missing, refuse to run, explain that the final summary depends on readiness validation, and tell the user to run `validate-topic-team` first.

If registration assurance is missing from the validation context, refuse to run, explain that the final summary must report authoritative topic refs or blockers, and tell the user to run `ensure-topic-registration` and then `validate-topic-team`.

## Summary Template

Write `isomer-topic-summary.md` with these sections:

```markdown
# Isomer Topic Summary

## Research Topic

## Topic Registration

## Topic Team

## Goal

## Working Logic

## Environment Setup

## Agent Workspace Layout

## Validation Status

## Blockers and Deferrals

## Next Actions
```

In `## Topic Registration`, summarize `topic_registration_status`, `registered_research_topic_ref`, `registered_topic_workspace_ref`, `registration_command_evidence`, `environment_binding_status`, and registration blockers. In `## Environment Setup`, summarize `topic_environment_status`, `env_gate_path`, `derived_gate_path`, service readiness status, setup commands, changed files, and blockers from `isomer-srv-topic-env-setup` when available. In `## Agent Workspace Layout`, distinguish worker-visible `repos/topic-main` and `agents/<agent-name>` worktrees from owner-preserved `records/*` and runtime-internal `runtime/*`.

## Guardrails

Do not claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from the summary.

Do not hide blockers in prose. Put them in `## Blockers and Deferrals`.

Do not include secrets, raw command payloads, live provider state, or transient adapter state in `isomer-topic-summary.md`.

# Finalize Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the topic overview, specialization outputs, durable setup records, Agent Workspace records, delegated Git-backed workspace manager evidence, validation status, blockers, deferrals, and next action refs.
3. Create or update `isomer-topic-summary.md` in the Topic Workspace root or selected provisional topic directory.
4. Include the sections in **Summary Template** and keep blockers visible when validation is incomplete, including missing delegated `isomer-admin-topic-workspace-mgr` evidence when Git-backed Agent Workspace worktrees were requested.
5. Report `isomer_topic_summary_path`, `topic_team_validation_status`, blockers, deferrals, and next operator action.
6. Stop at the final summary boundary unless the user explicitly asks for `approve-profile` or `materialize-profile`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step static finalization plan from the topic-team artifacts, setup records, validation outputs, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifact:

- `topic_team_validation_status` from `validate-topic-team`, including ready, ready-with-deferrals, or blocked status.

If validation status is missing, refuse to run, explain that the final summary depends on readiness validation, and tell the user to run `validate-topic-team` first.

## Summary Template

Write `isomer-topic-summary.md` with these sections:

```markdown
# Isomer Topic Summary

## Research Topic

## Topic Team

## Goal

## Working Logic

## Environment Setup

## Agent Workspace Layout

## Validation Status

## Blockers and Deferrals

## Next Actions
```

## Guardrails

Do not claim live team readiness, Workspace Runtime readiness, Agent Team Instance creation, adapter preflight, or launch readiness from the summary.

Do not hide blockers in prose. Put them in `## Blockers and Deferrals`.

Do not include secrets, raw command payloads, live provider state, or transient adapter state in `isomer-topic-summary.md`.

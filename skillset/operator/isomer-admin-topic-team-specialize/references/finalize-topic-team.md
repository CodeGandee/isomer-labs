# Finalize Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read the topic overview, specialization outputs, setup records, Agent Workspace records, validation status, blockers, deferrals, and next action refs.
2. Create or update `isomer-topic-summary.md` in the Topic Workspace root or selected provisional topic directory.
3. Include the sections in **Summary Template** and keep blockers visible when validation is incomplete.
4. Report `isomer_topic_summary_path`, `topic_team_validation_status`, blockers, deferrals, and next operator action.
5. Stop at the final summary boundary unless the user explicitly asks for `approve-profile`, `materialize-profile`, or `launch-team`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step finalization plan from the topic-team artifacts, setup records, validation outputs, and guardrails, then execute the plan.

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

Do not claim live launch readiness from the summary alone.

Do not hide blockers in prose. Put them in `## Blockers and Deferrals`.

Do not include secrets, raw command payloads, or transient adapter state in `isomer-topic-summary.md`.

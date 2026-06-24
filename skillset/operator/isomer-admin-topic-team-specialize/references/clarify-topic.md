# Clarify Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read `<topic-dir>/topic-def/topic-overview.md`, plus any user answers, source material, or newly supplied constraints.
3. Identify open questions that affect topic scope, objectives, assumptions, or template selection.
4. Ask the user only for the missing information needed to make the Research Topic actionable.
5. Update or report revisions to `topic-overview.md`, preserving previous assumptions unless the user corrects them.
6. Report the revised topic understanding, remaining open questions, provisional registration status, and whether `specialize-team` can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step clarification plan from the topic overview, user answers, and Project Config boundary, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifact:

- `<topic-dir>/topic-def/topic-overview.md` from `init-topic`.

If `topic-overview.md` does not exist, refuse to run, explain that there is no topic definition to clarify, and tell the user to run `init-topic` first.

## Guardrails

Do not specialize the team from this subcommand. Stop after topic clarification and route to `specialize-team` when the topic is ready.

Do not silently discard earlier assumptions. Mark corrected assumptions as revised.

Do not promote a provisional topic workspace seed into authoritative Project Manifest state.

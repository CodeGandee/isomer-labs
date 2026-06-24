# Clarify Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Read the specialization outputs: topic overview, copied template root, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, and draft profile summary.
3. Identify role, workflow, assumption, policy, binding, copied-material, or blocker questions that need user review.
4. Ask the user for focused revisions or decisions about the specialized topic team.
5. Update or report revisions to the copied material, specialization plan, `Final Report`, placeholder resolutions, deferrals, or draft profile inputs as needed.
6. Report `topic_team_revision_status`, changed paths, remaining blockers, validation refs, and whether setup can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step revision plan from the specialization outputs, requested changes, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifacts from `specialize-team`:

- `<topic-workspace>/team-profile/execplan/team-specialization-guide.md`.
- `<topic-workspace>/team-profile/execplan/team-specialization-plan.md` with a filled or pending `Final Report`.
- Draft profile or packet/profile input summary from `draft-profile`.

If any required specialization output is missing, refuse to run, explain which artifact is missing, and tell the user to run `specialize-team` first.

## Guardrails

Do not approve, materialize, or launch the team from this subcommand.

Do not change the source Domain Agent Team Template.

Do not hide unresolved launch blockers. Keep deferrals explicit.

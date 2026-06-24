# Specialize Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Confirm the Research Topic is clear enough to specialize. If not, route to `clarify-topic`.
3. Ask the user to select or confirm one Domain Agent Team Template when the template is not already clear.
4. Run `resolve-project`, `inspect-template`, and `resolve-context` to gather Project, topic, workspace, template, copied-material, policy, binding, and static setup refs.
5. Create or confirm `<topic-workspace>/team-profile/`, copy selected Domain Agent Team Template material into it, and use `<topic-workspace>/team-profile/execplan/` as the default copied template root for `deepsci-mini`.
6. Read `team-specialization-guide.md` in the copied template root, or create it with the generated-guide fenced block from the entrypoint when no source guide exists.
7. Create `team-specialization-plan.md` in the copied template root with the required checklist, planned edits, validation plan, and pending `Final Report`.
8. Run `map-placeholders`, adapt only copied template material according to the plan, fill the `Final Report`, and run `draft-profile`.
9. Report created or updated Topic Agent Team Profile Bundle inputs, copied template material, placeholder resolutions, deferrals, validation refs, and the next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step specialization plan from the topic material, selected template, helper subcommands, output contract, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifact:

- `<topic-dir>/topic-def/topic-overview.md` from `init-topic`, optionally revised by `clarify-topic`.

If `topic-overview.md` does not exist, refuse to run, explain that there is no topic definition to specialize against, and tell the user to run `init-topic` first.

## Guardrails

Specialize exactly one Research Topic and one Domain Agent Team Template at a time.

Do not edit the source Domain Agent Team Template. Adapt only copied material under the selected Topic Workspace.

Do not claim approval, materialization, setup readiness, or live operation from this subcommand. Route static setup and profile-material boundaries to `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, or `materialize-profile`.

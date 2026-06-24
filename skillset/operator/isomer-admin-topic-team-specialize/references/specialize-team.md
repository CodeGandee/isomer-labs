# Specialize Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Confirm the Research Topic is clear enough to specialize. If not, route to `init-topic` or `clarify-topic`.
2. Ask the user to select or confirm one Domain Agent Team Template when the template is not already clear.
3. Run `resolve-project`, `inspect-template`, and `resolve-context` to gather Project, topic, workspace, template, copied-material, policy, binding, and readiness refs.
4. Create or confirm `<topic-workspace>/team-profile/`, copy selected Domain Agent Team Template material into it, and use `<topic-workspace>/team-profile/execplan/` as the default copied template root for `deepsci-mini`.
5. Read `team-specialization-guide.md` in the copied template root, or create it with the generated-guide fenced block from the entrypoint when no source guide exists.
6. Create `team-specialization-plan.md` in the copied template root with the required checklist, planned edits, validation plan, and pending `Final Report`.
7. Run `map-placeholders`, adapt only copied template material according to the plan, fill the `Final Report`, and run `draft-profile`.
8. Report created or updated Topic Agent Team Profile Bundle inputs, copied template material, placeholder resolutions, deferrals, validation refs, and the next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step specialization plan from the topic material, selected template, helper subcommands, output contract, and guardrails, then execute the plan.

## Guardrails

Specialize exactly one Research Topic and one Domain Agent Team Template at a time.

Do not edit the source Domain Agent Team Template. Adapt only copied material under the selected Topic Workspace.

Do not claim approval, materialization, setup readiness, or launch from this subcommand. Route those boundaries to `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, `materialize-profile`, or `launch-team`.

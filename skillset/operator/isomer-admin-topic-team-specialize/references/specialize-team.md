# Specialize Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Confirm the Research Topic is clear enough to specialize. If not, route to `clarify-topic`.
3. Confirm registration evidence:
   - Require `ensure-topic-registration` evidence showing a manifest-backed Research Topic and Topic Workspace with no unresolved registration blockers.
   - If registration evidence is missing or blocked, refuse to run and tell the user to run `ensure-topic-registration` first.
4. Ask the user to select or confirm one Domain Agent Team Template when the template is not already clear.
5. Run `resolve-project`, `inspect-template`, and `resolve-context` to gather Project, registered topic, registered workspace, template, copied-material, policy, binding, and static setup refs.
6. Create or confirm copied team material:
   - Create or confirm `<topic-workspace>/team-profile/`.
   - Copy selected Domain Agent Team Template material into it.
   - Use `<topic-workspace>/team-profile/execplan/` as the default copied template root for `deepsci-mini`.
7. Read `team-specialization-guide.md` in the copied template root, or create it with the generated-guide fenced block from the entrypoint when no source guide exists.
8. Create `team-specialization-plan.md` in the copied template root with the required checklist, planned edits, validation plan, and pending `Final Report`.
9. Run `map-placeholders`, adapt only copied template material according to the plan, fill the `Final Report`, and run `draft-profile`.
10. Report specialization output:
   - Include created or updated Topic Agent Team Profile Bundle inputs, copied template material, placeholder resolutions, registration evidence, deferrals, validation refs, and the next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step specialization plan from the topic material, selected template, helper subcommands, output contract, and guardrails, then execute the plan.

## Prerequisite Artifacts

Required predecessor artifact:

- `topic.intent.overview` from `resolve-topic-intent`, optionally revised by `clarify-topic`.
- Registration assurance from `ensure-topic-registration`, including `registered_research_topic_ref`, `registered_topic_workspace_ref`, `topic_registration_status: registered`, and no unresolved `registration_blockers`.

If `topic.intent.overview` does not exist, refuse to run, explain that there is no topic definition to specialize against, and tell the user to run `resolve-topic-intent` first.

If registration assurance is missing or reports `topic_registration_status: blocked`, refuse to run, explain that specialization needs authoritative Project Manifest-backed topic refs, and tell the user to run `ensure-topic-registration` first.

## Guardrails

Specialize exactly one Research Topic and one Domain Agent Team Template at a time.

Do not edit the source Domain Agent Team Template. Adapt only copied material under the selected Topic Workspace.

Do not claim approval, materialization, setup readiness, or live operation from this subcommand. Route static setup and profile-material boundaries to `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, or `materialize-profile`.

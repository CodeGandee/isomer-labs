# Fast Forward

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Run `resolve-project` to select the Project, Research Topic, Topic Workspace, Domain Agent Team Template, profile bundle, and runtime refs.
2. Run `inspect-template` to understand template metadata, placeholders, role slots, Workflow Stages, workspace contracts, diagnostics, and copyable material.
3. Run `resolve-context` to gather Effective Topic Context, Workspace Runtime readiness, policy refs, Capability Binding refs, Skill Binding Projection refs, provider refs, and Gate policy refs.
4. Create or confirm `<topic-workspace>/team-profile/`, copy selected Domain Agent Team Template material into it, then use `<topic-workspace>/team-profile/execplan/` as the default copied template root for `deepsci-mini`.
5. Read `team-specialization-guide.md` in the copied template root, or create it with the generated-guide fenced block from the entrypoint when no source guide exists.
6. Create `team-specialization-plan.md` in the copied template root with the required checklist, planned edits, validation plan, and pending `Final Report`.
7. Run `map-placeholders`, then adapt only copied template material according to the plan.
8. Fill the `Final Report`, then run `draft-profile` to report Topic Team Instantiation Packet and Topic Agent Team Profile Bundle inputs.
9. Stop at specialization output. Run `approve-profile`, `materialize-profile`, or `launch-team` only when the user explicitly asks for that next boundary and required validation or approval inputs are available.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the selected topic, template, subcommands, output contract, and guardrails, then execute the plan.

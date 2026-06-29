# Specialize Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root, Research Topic, Topic Workspace, and requested Domain Agent Team Template ref.
2. Check Project validity and context with `check-project` and `show-context` when refs are unclear.
3. Confirm that the request is about adapting or instantiating a Domain Agent Team Template for one Research Topic.
4. Hand off to `isomer-admin-topic-team-specialize fast-forward` with the resolved Research Topic and Domain Agent Team Template refs.
5. Report the handoff target, resolved refs, blockers, and any Project readiness steps still needed before specialization can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project context, topic-team specialization boundary, and guardrails, then execute the plan.

## Guardrails

- Do not duplicate Topic Team Specialization logic in this skill.
- Do not hand off direct specialization requests to `adapt-team-template`; that is an internal stage owned by `isomer-admin-topic-team-specialize`.
- Do not edit Domain Agent Team Template source material from this subcommand.
- Do not launch a team from Project context alone.

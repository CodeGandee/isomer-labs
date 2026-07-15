# Specialize Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root, Research Topic, Topic Workspace, and requested Domain Agent Team Template ref.
2. Check Project validity and context with `check-project` and `show-context` when refs are unclear.
3. Confirm that the user explicitly invoked specialization or that the prompt or authoritative context establishes a formal Agent Team target and asks to adapt, deploy, specialize, instantiate, materialize, validate, repair, launch, or use that team. Accept a Domain Agent Team Template, Topic Agent Team Profile or Bundle, Topic Team Instantiation Packet, Agent Team Instance, selected formal-team material, or equivalent evidence; do not infer the route from manual Topic Actor research, generic topic preparation, launch-facing language, readiness gaps, missing summaries, or missing Agent Workspaces.
4. If reusable topic preparation evidence is missing, note that `isomer-op-topic-team-specialize fast-forward` will create or consume the required topic setup evidence before team-specific stages, or hand off to `isomer-op-topic-creator` when the user asked only for topic preparation.
5. Hand off to `isomer-op-topic-team-specialize fast-forward` with the resolved Research Topic and Domain Agent Team Template refs.
6. Report the handoff target, resolved refs, preserved Topic Actor context when present, blockers, and any Project readiness steps still needed before specialization can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project context, topic-team specialization boundary, and guardrails, then execute the plan.

## Guardrails

- DO NOT duplicate Topic Team Specialization logic in this skill.
- DO NOT hand off direct specialization requests to `adapt-team-template`; that is an internal stage owned by `isomer-op-topic-team-specialize`.
- DO NOT route manual research, human-orchestrated Topic Actor setup, or Topic Actor Workspace materialization here unless the user also asked for formal Topic Team Specialization.
- DO NOT edit Domain Agent Team Template source material from this subcommand.
- DO NOT launch a team from Project context alone.

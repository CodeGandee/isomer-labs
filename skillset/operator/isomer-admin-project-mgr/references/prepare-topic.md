# Prepare Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root, selected Research Topic, and selected Topic Workspace through Project Manifest-backed context.
2. Check Project health and selected Effective Topic Context with `check-project` and `show-context` when refs are unclear.
3. Confirm that the request is about reusable topic preparation for manual research, human-orchestrated research, or later team specialization rather than direct Domain Agent Team Template adaptation.
4. Hand off to `isomer-admin-topic-prepare` with the selected Research Topic, Topic Workspace, requested setup scope, and any explicit opt-out for the default `operator` Topic Actor Workspace.
5. Report the handoff target, resolved refs, requested operator actor posture, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from Project context, topic preparation boundaries, and guardrails, then execute the plan.

## Guardrails

- Do not duplicate common topic preparation logic in this skill.
- Do not imply Topic Team Specialization from a manual research or human-orchestrated request.
- Do not create Topic Actor bindings here; delegate Topic Actor work to `isomer-admin-topic-workspace-mgr` through the preparation skill.
- Do not create `topic.repos.main` or repair topic environment readiness from this subcommand.

# Prepare Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Resolve the Project root, selected Research Topic, and selected Topic Workspace through Project Manifest-backed context.
2. Check Project health and selected Effective Topic Context with `check-project` and `show-context` when refs are unclear.
3. If the request is about blank-state topic creation, Topic Actor-ready setup, or human-orchestrated research, hand off to `isomer-op-topic-creator fast-forward`, `isomer-op-topic-creator step-by-step`, or `isomer-op-topic-creator run-to <procedural-subcommand>` with the selected Project, Research Topic, Topic Workspace, requested setup scope, requested actors, and any explicit opt-out for the default `operator` Topic Actor Workspace.
4. Report the handoff target, resolved refs, requested operator actor posture, blockers, and next operator action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from Project context, topic preparation boundaries, and guardrails, then execute the plan.

## Guardrails

- DO NOT duplicate topic creation or common topic preparation logic in this skill.
- DO NOT imply Topic Team Specialization from a manual research or human-orchestrated request.
- DO NOT create Topic Actor bindings here; route normal setup through `isomer-op-topic-creator` and let it delegate Topic Actor work to `isomer-op-topic-mgr`.
- DO NOT create `topic.repos.main` or repair topic environment readiness from this subcommand.

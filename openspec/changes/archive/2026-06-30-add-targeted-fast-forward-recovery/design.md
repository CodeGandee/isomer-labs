## Context

`isomer-admin-topic-team-specialize` has a long procedural chain. Several subcommands require predecessor artifacts from earlier stages, such as `topic.intent.overview`, registration assurance, topic environment setup evidence, specialized team material, or Agent Workspace evidence. The current text tells the agent to refuse when those artifacts are absent and to name earlier subcommands. That behavior is correct about ownership, but poor as an operator experience: the user already selected the desired target stage, and the skill knows the canonical predecessor path.

## Goals / Non-Goals

**Goals:**

- Define a shared prerequisite recovery policy for blocked Topic Team Specialization subcommands.
- Let the operator fast-forward to the attempted subcommand when missing predecessor artifacts can be created by the canonical flow.
- Make inclusive recovery the default: prepare missing predecessors and then run the attempted subcommand.
- Allow exclusive recovery: prepare missing predecessors and stop before the attempted subcommand.
- Preserve explicit consent before workspace mutation when the user did not already authorize automatic progress.

**Non-Goals:**

- Do not change the Project Manifest, Workspace Path Resolution, or topic workspace storage model.
- Do not add a separate Python CLI command for targeted fast-forward.
- Do not make procedural subcommands silently create all missing artifacts without reporting the recovery mode.
- Do not change the full `fast-forward` path that runs through final topic-team summary output.

## Decisions

1. Add one shared recovery rule at the skill entrypoint.

   The entrypoint should define targeted fast-forward once, then subcommand pages can refer to that rule. This avoids repeating slightly different refusal language in every page.

2. Treat targeted fast-forward as bounded execution, not as full specialization.

   The target is the subcommand the user attempted to run. Inclusive mode runs the canonical path through the target. Exclusive mode runs the canonical predecessor path and stops before the target. The existing full `fast-forward` still means the end-to-end path through `finalize-topic-team`.

3. Ask before mutation unless permission is already clear.

   Targeted recovery may create intent files, register a Topic Workspace, call setup services, create derived gates, or prepare Agent Workspaces. The skill should present the missing prerequisites, the intended path, and the inclusive default before it mutates the workspace.

4. Keep prerequisite ownership intact.

   A blocked subcommand should not perform predecessor work internally. It should route to targeted fast-forward, which runs the canonical predecessor subcommands in order. This keeps each stage's responsibility clear.

## Risks / Trade-offs

- [Risk] Targeted fast-forward could feel like the subcommand is doing too much. → Mitigation: require the response to name the recovery path and state whether the target is included.
- [Risk] Users may expect `fast-forward` to always mean the full path. → Mitigation: call the bounded form `targeted fast-forward` and distinguish it from full `fast-forward` in skill text.
- [Risk] A prerequisite may require clarification rather than automatic creation. → Mitigation: targeted fast-forward stops at the same clarification blockers as the normal flow and reports the next question or action.
- [Risk] Subcommand pages may keep stale hard-refusal wording. → Mitigation: update the guardrail and the prerequisite failure text on affected subcommands to reference the shared recovery policy.

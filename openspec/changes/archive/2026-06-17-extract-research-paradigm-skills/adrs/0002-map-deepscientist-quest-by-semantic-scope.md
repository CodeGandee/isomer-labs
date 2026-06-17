# Map DeepScientist Quest by Semantic Scope

## Status

accepted

## Context

DeepScientist uses `quest` broadly. Depending on context, it can mean a research goal, lifecycle object, filesystem root, persisted state, current stage, branch, runtime attempt, or active runner context.

Isomer Labs splits those responsibilities across Research Thread, Research Goal, Research Task, Research Branch, Isomer Workspace, Workspace Runtime, Run, and Agent Workspace.

## Decision

Map each DeepScientist `quest` reference by semantic scope, not by word replacement.

| DeepScientist scope | Isomer framing |
| --- | --- |
| User-facing lifecycle, pause, resume, archive, completion, overall steering | Research Thread |
| Initial objective, prompt goal, startup contract intent | Research Goal |
| Bounded assignment handled in one execution area | Research Task |
| Forked line of work or route under consideration | Research Branch |
| One runner attempt or execution episode | Run |
| Filesystem area for one bounded research task | Isomer Workspace |
| Persistent state substrate, recovery state, records, refs, validation state | Workspace Runtime |
| Per-agent scratch, owned local outputs, local runtime traces | Agent Workspace or Agent Runtime |
| Literal Git branch or Git worktree | Git branch or Git worktree, only when the implementation is actually Git |

When a DeepScientist source path is tied to a quest root, such as `<quest_root>/.ds/runs/<run_id>/result.json`, the migrated skill must not guess the Isomer path. It should refer to the relevant Isomer concept and mark the concrete path as `yet-to-be-determined`.

## Considered Options

- Map every `quest` mention to Research Thread.
- Map every `quest` mention to Isomer Workspace.
- Keep `quest` as a compatibility term.
- Map by semantic scope.

## Consequences

- Skills can describe lifecycle, storage, execution, and branching without overloading one term.
- `quest` should not appear in skill instructions except in provenance, source quotes, or explicit mapping notes.
- Research Thread remains the lifecycle object. Isomer Workspace remains the task storage and runtime owner. Run remains the execution attempt.
- If a source behavior depends on a DeepScientist quest directory layout, the layout is an unsettled surface, not a concept.

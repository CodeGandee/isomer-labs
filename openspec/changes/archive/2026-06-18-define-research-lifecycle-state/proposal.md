## Why

The research-paradigm skillset now has settled workspace paths and durable recording contracts, but its execution-level vocabulary still depends on unsettled lifecycle placeholders for Stage Cursor, Agent Team State, and branching policy. This blocks the skills from consistently representing Research Topic, Research Inquiry, Research Task, Run, and Agent Team Instance progress without falling back to stale terms such as Research Thread, Research Branch, or Isomer Workspace.

## What Changes

- Add a Research Lifecycle State contract that defines identity, state, and allowed relationships for Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Research Inquiry Relationship, and Agent Team Instance lifecycle state.
- Define how Research Inquiry Relationships capture generated or decomposed questions without forcing all exploration paths into a tree.
- Define branch, pause, resume, supersede, block, finalize, and archive transitions at the appropriate lifecycle levels.
- Define Topic-level parallel execution across Agent Team Instances and Task-level parallel execution across Agent Instances, while explicitly excluding Research Inquiry as a parallel execution scope.
- Settle `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching` by mapping them to accepted lifecycle-state contracts.
- Update research-paradigm skill requirements and references to use Research Topic, Research Inquiry, Research Task, Topic Workspace, Workflow Stage Cursor, Research Inquiry Relationship, and Agent Team Instance lifecycle state consistently.
- Keep command execution, scheduler policy, Capability Binding, Skill Binding, literature provider, baseline-waiver policy, and cost/privacy Gate thresholds out of scope.

## Capabilities

### New Capabilities

- `research-lifecycle-state`: Defines research execution levels, lifecycle states, transition rules, Workflow Stage Cursor, Research Inquiry Relationship behavior, and Agent Team Instance lifecycle state.

### Modified Capabilities

- `research-paradigm-skills`: Consume the accepted lifecycle contract, remove stale lifecycle vocabulary, replace settled lifecycle TBD placeholders, and keep unrelated TBD placeholders explicit.
- `research-recording-contracts`: Clarify that durable record lifecycle refs point to accepted lifecycle-state objects rather than placeholder-level lifecycle surfaces.

## Impact

- Main specs under `openspec/specs/`.
- Shared and per-skill research-paradigm references under `skillset/research-paradigm/`.
- The shared TBD registry for `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching`.
- The skill-gap plan in `context/plans/research-paradigm-skill-gaps.md`.

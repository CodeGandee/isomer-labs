# Agent Team Instance Inquiry Refs

## Question Asked

Should `Agent Team Instance lifecycle state` include active or relevant `Research Inquiry` refs?

## Decision

Use optional active or relevant `Research Inquiry` refs as context and routing anchors on `Agent Team Instance lifecycle state`. These refs do not make Research Inquiry a parallel execution scope.

## Rationale

The project glossary defines Research Inquiry as a question or line of inquiry under a Research Topic. It can own tasks and relationships, but it is not a parallel execution scope. The glossary also defines topic-level parallel execution as multiple Agent Team Instances under one Research Topic, usually comparing team profiles, strategies, or independent inquiry paths.

The OpenSpec change already allowed topic-level parallel teams to record active Research Inquiry refs, but the general Agent Team Instance state scenario did not name those refs. This decision makes the state shape explicit: an Agent Team Instance can say which inquiry neighborhood it is currently advancing, while execution scope remains either Topic-level across Agent Team Instances or Task-level across Agent Instances inside one team.

## Accepted Behavior

- `Agent Team Instance lifecycle state` MAY include zero or more active or relevant `Research Inquiry` refs.
- `Research Inquiry` refs on an Agent Team Instance are context and routing anchors, not execution ownership boundaries.
- Topic-level parallel execution remains multiple Agent Team Instances under one Research Topic.
- Task-level parallel execution remains multiple Agent Instances working on one Research Task inside the selected Agent Team Instance.
- A Research Task still belongs to one Research Inquiry and one Topic Workspace.
- A Research Inquiry still must not carry parallel execution state.

## Alternatives Rejected

- Do not include Research Inquiry refs on Agent Team Instance state. This keeps the record smaller, but loses the direct inquiry anchor needed to distinguish parallel teams working under the same topic.
- Require exactly one active Research Inquiry per Agent Team Instance. This is too restrictive for teams that work across related inquiry neighborhoods or transition between linked inquiries during one topic-level execution.

## Evidence

- `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` defines Research Inquiry as a question object, not a parallel execution scope.
- `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md` defines topic-level parallel execution across Agent Team Instances and task-level parallel execution across Agent Instances.
- `openspec/changes/define-research-lifecycle-state/specs/research-lifecycle-state/spec.md` already records active Research Inquiry refs for topic-level parallel execution, so the base Agent Team Instance state needs the same boundary stated explicitly.

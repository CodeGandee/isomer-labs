## Context

Workspace Path Resolution has settled ordinary locations, and Research Recording Contracts have settled durable Artifacts, Provenance Records, Evidence Items, Findings, Research Claims, Decision Records, and Gates. The remaining research-paradigm skill gaps now sit at the lifecycle layer: the skills name Research Topic, Research Inquiry, Research Task, Run, Workflow Stage, Research Inquiry Relationship, and Agent Team Instance, but `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching` are still open TBDs.

The current domain language has already moved away from Research Goal, Research Thread, Research Branch, Isomer Workspace, and branch-as-tree assumptions. A Research Topic is the root research question or cause that initiates work. A Research Inquiry is any question decomposed or generated to work out the topic. A Research Task is concrete development, experiment, analysis, writing, review, or validation work needed to answer an inquiry. A Run is one execution attempt or bounded work pass. Agent Teams can parallelize at Topic scope or at Task scope, but not at Research Inquiry scope.

The implementation should update specs and skill documents only. It should not define runtime command execution, scheduling loops, Capability Binding, Skill Binding, literature providers, baseline-waiver policy, or cost/privacy thresholds.

## Goals / Non-Goals

**Goals:**

- Define lifecycle identities and state boundaries for Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Research Inquiry Relationship, and Agent Team Instance lifecycle state.
- Settle `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching`.
- Replace stale lifecycle terms in main specs and active research-paradigm skills.
- Preserve the accepted rule that Research Inquiry is not a parallel execution scope.
- Keep lifecycle refs compatible with Workspace Path Resolution and Research Recording Contracts.
- Keep unresolved execution, scheduler, capability, literature, baseline-waiver, and cost/privacy surfaces explicitly marked as TBD.

**Non-Goals:**

- Do not define the Execution Adapter command API or command permission model.
- Do not define scheduler policy, continuation automation, queue semantics, or watchdog behavior.
- Do not define Skill Binding, Capability Binding, credential binding, provider binding, or package-manager binding schemas.
- Do not define literature search provider behavior.
- Do not define baseline-waiver or cost/privacy Gate thresholds.
- Do not implement application code or persistent storage migrations.

## Decisions

### Decision 1: Model Lifecycle as Levels, Not as Source Runtime Aliases

The accepted levels are Research Topic, Research Inquiry, Research Task, and Run. Research Topic replaces the former goal-level language. Research Inquiry replaces thread-level language. Research Inquiry Relationship replaces branch language when one inquiry follows, decomposes, contrasts, narrows, broadens, supersedes, duplicates, or depends on another inquiry. Topic Workspace replaces Isomer Workspace.

Alternative considered: keep Research Thread and Research Branch as compatibility synonyms. Rejected because synonyms would keep stale skill language alive and make validation weaker.

### Decision 2: Make Research Inquiry Relationships a Graph

Research Inquiry Relationships are directed records between lifecycle objects, usually inquiry-to-inquiry but also topic-to-inquiry when an inquiry is first generated. They must not imply that all inquiry relationships form a single tree. A set of related inquiries can be cyclic, cross-linked, merged, or abandoned without becoming a named branch collection.

Alternative considered: define Branch as a collection of child inquiries. Rejected because the user's domain model says exploration paths may not become a tree, and because branch collections would encourage agents to invent structure where a relation graph is enough.

### Decision 3: Split State by Level

Each lifecycle object has a small explicit status set:

- Research Topic: `open`, `active`, `paused`, `blocked`, `finalized`, `archived`.
- Research Inquiry: `open`, `active`, `answered`, `blocked`, `superseded`, `withdrawn`.
- Research Task: `planned`, `ready`, `active`, `blocked`, `completed`, `failed`, `cancelled`, `superseded`.
- Run: `planned`, `running`, `succeeded`, `failed`, `cancelled`, `stale`.
- Workflow Stage Cursor: `active`, `recommended`, `blocked`, `paused`, `completed`, `superseded`.
- Agent Team Instance lifecycle state: `planned`, `active`, `paused`, `blocked`, `completed`, `stopped`, `archived`.

These statuses are lifecycle semantics, not scheduler instructions. A later scheduler contract can map runtime queues or continuation policies onto these states without changing this contract.

Alternative considered: define one shared status enum for all objects. Rejected because the meaning of `answered`, `succeeded`, and `completed` differs across inquiry, run, and task levels.

### Decision 4: Define Workflow Stage Cursor as Routing State

Workflow Stage Cursor records the current or recommended research stage, why that stage is selected, what lifecycle object owns it, what evidence or Decision Record supports it, and whether it is active, blocked, paused, completed, or superseded. It does not schedule future work and does not auto-continue an agent.

Alternative considered: use Workflow Stage Cursor as a scheduler command. Rejected because `policy-scheduler` remains open, and combining routing state with scheduling would settle too much at once.

### Decision 5: Define Agent Team Instance State Without Binding Details

Agent Team Instance lifecycle state records which Research Topic or Research Task the team instance is advancing, whether it is active, paused, blocked, completed, stopped, or archived, and which Agent Instances are participating when that information is already known. It may reference active or relevant Research Inquiries as context and routing anchors, especially for topic-level parallel teams working through different inquiry neighborhoods, but those refs do not make Research Inquiry a parallel execution scope. It may also reference Agent Workspace, Agent Runtime, Run, Workflow Stage Cursor, Decision Record, Gate, and Provenance Record objects. It must not define Skill Binding, Capability Binding, credential binding, or concrete execution permissions.

Alternative considered: define Agent Team Instance as a full runtime object with concrete tool and credential bindings. Rejected because that belongs to the later Capability and Skill Binding contract.

### Decision 6: Define Parallelism at Topic and Task Scope Only

Topic-level parallelism means multiple Agent Team Instances can work under the same Research Topic, usually on different inquiry neighborhoods or strategies. Task-level parallelism means multiple Agent Instances inside one Agent Team Instance can work on different parts of a Research Task. Research Inquiry is not a parallel execution scope; it is a question object that can own or relate tasks.

Alternative considered: allow Research Inquiry-level parallel execution. Rejected because the user explicitly ruled it out, and because it would blur question decomposition with execution planning.

Clarification accepted during design exploration: Agent Team Instance lifecycle state may carry optional active or relevant Research Inquiry refs as context and routing anchors. These refs identify the inquiry neighborhood a team is advancing; they do not create inquiry-level execution ownership, scheduling, or parallelism.

### Decision 7: Treat Branching Policy as Relationship Promotion Policy

The settled replacement for `policy-branching` is a policy for when to create, update, supersede, or reject Research Inquiry Relationships. It requires agents to record the relation type, rationale, evidence or Finding refs, source and target lifecycle refs, and a Decision Record only when a meaningful route choice was made.

Alternative considered: make every generated inquiry a Decision Record. Rejected because this would overuse decisions for ordinary decomposition and make Gate/Decision semantics noisy.

## Risks / Trade-offs

- Over-settling scheduler behavior through lifecycle states -> Keep scheduler language out of status definitions and leave `policy-scheduler` open.
- Under-specifying Agent Team Instance state -> Define lifecycle and participation refs now, but leave bindings and permissions for Stage 4.
- Stale terms remain in local skill copies -> Include explicit search tasks for Research Goal, Research Thread, Research Branch, and Isomer Workspace.
- Branching policy becomes too strict and slows exploration -> Make relationship recording lightweight and require Decision Records only for meaningful choices.
- Parallel execution rules conflict with later execution adapters -> Define scope only, not command execution, queues, or resource scheduling.

## Migration Plan

1. Add a new main `research-lifecycle-state` spec from the delta spec.
2. Update `research-paradigm-skills` so accepted lifecycle terms replace stale vocabulary and resolved lifecycle TBDs are not open placeholders.
3. Update `research-recording-contracts` so lifecycle refs point to accepted lifecycle-state objects.
4. Update the shared TBD registry and local `isomer-research-contract.md` copies to map `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching` to Research Lifecycle State.
5. Update stage-specific skills and references that route between intake, scout, baseline, idea, optimize, experiment, analysis, decision, write, review, rebuttal, and finalize.
6. Update the skill-gap plan after implementation.
7. Validate with OpenSpec, placeholder searches, stale-term searches, and diff review.

Rollback is documentation-only: revert the spec and skill-document changes if the lifecycle contract proves wrong before implementation ships.

## Open Questions

- Should `Run` remain in this lifecycle contract as a lifecycle object only, or should detailed Run execution fields wait entirely for Execution Adapter? This design keeps Run identity and status here and defers command fields.
- Should Agent Team Instance state include named Agent Roles immediately, or only Agent Instance refs? This design allows role refs when known but leaves role-binding schema to the later Capability and Skill Binding contract.

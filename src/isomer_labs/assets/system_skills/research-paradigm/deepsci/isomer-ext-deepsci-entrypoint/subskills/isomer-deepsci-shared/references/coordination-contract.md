# Coordination Contract

Use this reference when production DeepSci research skills need shared vocabulary or route discipline before storage binding exists.

## Workflow

When this reference is used, execute the following steps in order.

1. **Name the shared object**. Identify whether the object is a workspace bootstrap, research frame, comparator contract, selected hypothesis, optimization frontier, experiment contract, experiment result, analysis finding, science validity note, route decision, or final summary.
2. **Keep ownership clear**. Name the skill that produces the object and the skill that consumes it.
3. **Route bootstrap work**. Use `isomer-deepsci-workspace-mgr` when the object is the post-preparation workspace bootstrap, placeholder binding registry, topic-level placeholder binding index, semantic surface plan, Topic Actor Workspace access plan, Agent Workspace access plan, validation report, or bootstrap blocker.
4. **Keep storage unresolved**. Do not assign concrete paths, Artifact kinds, schema rows, or runtime labels unless a storage-binding pass has already approved them.
5. **Classify prerequisite routes**. When the consumer lacks an input with a known producer, return `paused` prerequisite recovery and use `prerequisite-recovery.md`. Reserve `blocked` for an unavailable external state change.
6. **Record route meaning**. If the object changes the next route, state the evidence basis, rejected alternatives, blocker if any, next action, and original target resume point.
7. **Preserve controller boundaries**. During explicitly authorized run-to traversal, let the current agent coordinate separate focused-skill or pass invocations without transferring ownership, skipping callbacks or Gates, merging Runs, or adding loops to a recipe.
8. **Return the shared contract**. Give the semantic object id, required content, producer, consumer, prerequisite status, and unresolved binding status.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step coordination plan from this reference and `semantic-placeholders.md`, then execute the plan.

## Rules

- Shared vocabulary does not replace domain skill judgment.
- Workspace bootstrap questions route to `isomer-deepsci-workspace-mgr`; shared only names the semantic object.
- When the current cwd is a Topic Actor Workspace, include the selected Topic Actor context and use actor metadata in accepted-record command guidance.
- When the current cwd is a formal Agent Workspace, include real formal agent context only if the work belongs to that Agent Instance or Agent Team Instance.
- When the current cwd is `topic.repos.main`, treat it as the integration surface and Git anchor, then ask the bootstrap manager to identify the selected Topic Actor or formal agent context before durable writes.
- A semantic placeholder names meaning, not storage.
- A route decision must be justified by evidence or a blocker.
- The owning skill remains accountable for the handoff content it produces.
- An ordinary target request pauses before prerequisite mutation; only explicit target-scoped run-to authorization lets the external controller consume a producer route.
- Every producer retains separate callbacks, quality gates, durable writes, terminal reports, and Run identity.

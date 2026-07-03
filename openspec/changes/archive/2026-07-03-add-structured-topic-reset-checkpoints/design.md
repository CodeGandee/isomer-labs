## Context

Topic Creator and Topic Team Specialization can bring a Topic Workspace to a ready state before research begins. After that boundary, research activity can write structured research records, generated Markdown views, runtime lifecycle rows, View Manifests, and actor or agent support material. Today there is no durable reset anchor that tells an operator which parts of the Topic Workspace belong to initialization and which parts were produced by later research.

The new structured research record infrastructure already provides JSON Schema validation, format profiles, generated Markdown review views, and topic-scoped Workspace Runtime persistence. This change uses that path for reset checkpoints instead of Git. The reset contract must be inspectable by agents, deterministic in JSON output, and safe enough to run as a dry-run plan before any destructive mutation.

## Goals / Non-Goals

**Goals:**

- Record a post-initialization/pre-research checkpoint as structured, topic-scoped state.
- Generate a reset plan that classifies records and files as preserve, delete, regenerate, skip, or blocked.
- Apply an approved reset plan using Workspace Runtime updates and semantic-label-derived file operations.
- Keep reset behavior compatible with manual Topic Actor research and formal Topic Agent Team preparation.
- Reset non-preserved post-checkpoint contents under managed Topic Actor and Topic Agent workspace roots.
- Make Topic Creator and Topic Manager guidance point operators to the checkpoint and plan records when restarting research.
- Let later research-preparation workflows explicitly extend the checkpoint if their setup should survive reset.

**Non-Goals:**

- No Git operations of any kind: no `git stash`, project-root tracking, branch reset, commit, tag, or ref management.
- No retained state for reset candidates; preservation requires checkpoint inclusion or an explicit checkpoint update.
- No hidden deletion of unknown files, tmp contents, external repositories, secrets, live adapter state, or running agents.
- No attempt to recreate machine-global environments, dependency caches, or system package state.
- No automatic research rerun after reset; this only restores the Topic Workspace to a restartable baseline.

## Decisions

### Decision: Store Reset Anchors as Structured Records Plus Runtime Rows

Use dedicated Workspace Runtime rows for checkpoint, reset plan, and reset outcome metadata, and create matching structured records for the agent-readable payload and generated Markdown review view.

Runtime rows make topic scoping, listing, validation, and reset application deterministic. Structured records make the checkpoint readable through the existing record workflow and keep payload evolution behind format profiles.

Alternative considered: store only Markdown reset notes. That is easy to inspect but too weak for deterministic reset planning, validation, and future CLI automation.

### Decision: Treat Checkpoints as a Boundary, Not a Snapshot of Every Byte

A checkpoint records readiness evidence, semantic labels, runtime high-watermarks, lifecycle record ids to preserve, structured payload ids to preserve, generated view paths to preserve, and support-surface policies. It does not try to copy every file under the Topic Workspace.

This matches Isomer's domain model: accepted research truth lives in Workspace Runtime and topic records, while tmp surfaces and actor scratch material are local support material. Unknown or unmanaged files become blockers or explicit preserve decisions rather than silently deleted material.

Alternative considered: copy the entire Topic Workspace into a backup directory. That captures more bytes but mixes generated caches, nested repositories, secrets, tmp, and runtime internals into a large opaque artifact that agents cannot reason about safely.

### Decision: Make Checkpoint Extension Explicit and Owned by the Preparing Workflow

Topic Creator `finalize` creates the first operator-level checkpoint. Later preparation workflows, including research-paradigm v2 bootstrap or skill-specific preparation, may update the checkpoint with their own preserved records and generated views when they want that preparation to survive reset.

The dependency points one way: operator skills do not need to know research-paradigm skills, while research-preparation skills may depend on the checkpoint API if they want durable preservation. If they do not update the checkpoint, reset planning treats their outputs as post-checkpoint state; after reset, that preparation must be run again.

Alternative considered: automatically infer all preparation records as preserved. That would reduce redo work, but it would require the reset engine to guess domain-specific intent and would couple operator reset logic to research skill semantics.

### Decision: Make Reset Plan Approval Explicit

`plan` must be read-only. `apply` must require a specific plan id and explicit confirmation. The plan records every proposed mutation and blocker before the system mutates any state.

This follows existing cleanup and deletion patterns in the project. It also gives agents a stable artifact to inspect, review, and hand to the user before restart.

Alternative considered: a single `reset --to <checkpoint>` command. That is shorter, but it hides destructive details and makes accidental loss more likely.

### Decision: Use Semantic Labels for File Mutations

Reset file operations must be derived from Workspace Path Resolution outputs such as `topic.records.artifacts`, `topic.records.views`, `topic.records.runs`, `topic.actors.workspace`, and `agent.workspace`. The reset engine must not use hard-coded default paths or sibling-directory scans as authority.

Semantic labels preserve non-default layout support and let validation explain path-source problems before applying changes.

Alternative considered: hard-code the default `isomer-content/topic-ws/<topic>/...` layout. That would be simpler but would violate the existing path-resolution contract.

### Decision: Reset Managed Actor and Agent Workspaces Broadly

In the first version, the reset plan treats non-preserved contents under resolved managed `topic.actors.workspace` and `agent.workspace` roots as destructive reset candidates. The plan preserves root directories and checkpoint-preserved baseline files, then marks all other post-checkpoint files and directories under those managed roots for deletion.

This makes reset useful for both manual Topic Actor work and formal Topic Agent Team work, where local notes, scratch files, and generated support artifacts often drive later behavior. Material outside resolved managed roots remains out of scope and becomes a blocker or explicit preserve decision.

Alternative considered: leave actor-local material untouched by default. That is safer for early implementation, but it would often fail to restore the Topic Workspace to the post-initialization state the operator expects.

### Decision: Destructively Delete Unpreserved Post-Checkpoint State

Research records, runtime rows, structured payloads, generated Markdown views, and managed support material created after the checkpoint are deleted during reset apply when the checkpoint or a later checkpoint update did not preserve them. Checkpoint, Topic Creator setup, Topic Team Specialization setup, reset plans, and reset outcome records are preserve candidates by default.

This makes reset a true return to the selected baseline. Auditability comes from the approved reset plan and reset outcome record, which list deleted ids, deleted paths, skipped actions, failed actions, and diagnostics.

Alternative considered: retain post-checkpoint rows with tombstone statuses. That would preserve provenance inside Workspace Runtime, but it would leave unpreserved research-preparation state behind and weaken the restart contract. The chosen behavior is destructive deletion with an explicit preflight plan and outcome record.

## Risks / Trade-offs

- Reset planning may miss unmanaged files that are outside semantic labels -> Treat unmanaged discovered files and actor/agent material outside managed roots as blockers or explicit preserve entries, never silent deletions.
- Destructive deletion is irreversible -> Require read-only planning, explicit plan id, explicit confirmation, stale-plan rejection, and an outcome record that names every applied or failed deletion.
- Runtime high-watermarks can be hard to compare after schema evolution -> Store both ids/timestamps and schema version, and make unsupported versions block reset apply.
- A reset can conflict with running agents or live adapter state -> Require live-run and adapter-state preflight checks before apply.
- Generated Markdown views may drift from structured payloads before reset -> Use existing structured payload validation and rendered digest checks when planning.
- The first implementation may not cover every future runtime table -> Version checkpoint payloads and make unhandled table names block apply rather than skipping them.

## Migration Plan

1. Add new runtime schema tables and dataclasses for reset checkpoints, reset plans, and reset outcomes.
2. Add DeepScientist artifact format profiles for checkpoint, reset plan, and reset outcome payloads.
3. Add Python APIs to create/update checkpoints, plan resets, show/list checkpoints, show plans, and apply approved plans.
4. Add `isomer-cli project topic-reset ...` commands with deterministic JSON output.
5. Update Topic Creator and Topic Manager guidance to create/check/read reset checkpoints at the post-initialization boundary without referencing research-paradigm skills.
6. Extend runtime validation to report stale checkpoints, missing preserved records, invalid reset plans, and forbidden Git-operation metadata.

Rollback is ordinary code rollback plus ignoring new runtime rows. Existing Topic Workspaces without reset tables continue to initialize/reopen through schema migration. Reset apply remains opt-in, so deployment does not mutate existing workspaces.

## Resolved Questions

- Resolved: the first checkpoint is created by Topic Creator `finalize` from operator-level readiness evidence, without depending on research-paradigm skill knowledge.
- Resolved: later research-preparation workflows must explicitly update the checkpoint to preserve their own setup; otherwise reset deletes that setup and it must be redone.
- Resolved: reset apply destructively deletes unpreserved post-checkpoint reset candidates; it does not retain them.
- Resolved: reset treats all non-preserved post-checkpoint contents under managed Topic Actor and Topic Agent workspace roots as destructive reset candidates.

# Prerequisite Recovery

Use this reference when a requested DeepSci skill or single-pass recipe lacks an accepted input that another known in-scope owner can produce or repair.

## Workflow

When this reference is used, execute the following steps in order.

1. **Capture the original target**. Name the focused skill or pipeline pass, its acceptance condition, current durable refs, and whether the user explicitly authorized run-to recovery.
2. **Preflight current state**. Run latest-context preflight, apply Worker Output Policy, resolve placeholder bindings, and identify accepted inputs, producer routes, callbacks, Gates, and storage posture before target mutation.
3. **Classify the gap**. A missing or stale input with a known in-scope producer yields `paused` prerequisite recovery. Reserve `blocked` for an unavailable external state change or an invalid state with no authorized repair owner.
4. **Prompt ordinary requests**. Before prerequisite mutation, recommend the dependency order and offer Run to the target, Execute the next prerequisite only, Inspect or choose another route, and Stop.
5. **Plan an authorized closure**. After explicit target-scoped run-to authorization, use the native planning tool to maintain the transitive prerequisite closure and original target.
6. **Invoke focused owners separately**. Preserve each skill's latest-context preflight, Worker Output Policy, begin and end callbacks, placeholder bindings, quality gates, durable writes, and terminal report. A pipeline recipe remains single-pass and linear.
7. **Refresh and resume**. Validate returned durable refs before the controller invokes another focused skill or a new recipe pass. Resume the original target only when its accepted inputs are current.
8. **Stop at the target or protected boundary**. Pause for human Gates, material scientific choices, destructive or irreversible actions, credentials or restricted data, license decisions, unexpected resources, public exposure, publication, or submission. Do not continue beyond the original target.

If the task does not map cleanly to these steps, use the native planning tool to build a target-scoped plan from the current context snapshot, focused-skill ownership, known producer routes, and nondelegable boundaries, then execute it or pause at the first protected boundary.

## Authorization Scope

An ordinary `do <task>` request authorizes the named target only. It does not authorize prerequisite research, experiment, repair, analysis, drafting, or finalization. Explicit `run to <target>`, `automate the prerequisites and then do <target>`, a `yes to all` response to the recovery prompt, or equivalent language authorizes routine in-scope prerequisites and the target.

Run-to is prompt-scoped and target-scoped. It is not global, session-wide, a CLI flag, Project setting, or Run-level Control Mode. It ends when the target completes, the user changes it, progress reaches a nondelegable boundary, or no route produces new accepted state.

## Controller Boundary

The current agent may act as the external controller after explicit run-to authorization. It consumes a focused skill or pipeline terminal report only after recording it, validating accepted refs, and refreshing current state. It must invoke each prerequisite skill or pass under its own ownership contract and keep separate Runs, terminal reports, callbacks, Gates, Artifacts, and provenance.

The controller must not insert backward edges or retries into a pipeline recipe. When a pass recommends work outside its remaining linear stages, the pass ends. The controller may invoke a separate focused skill or a new pass, then resume or restart the original target from validated refs if its recipe permits that entry point.

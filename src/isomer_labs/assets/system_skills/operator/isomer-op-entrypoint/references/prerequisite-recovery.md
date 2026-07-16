# Prerequisite Recovery

## Workflow

1. **Capture the selected target**. Preserve the user's original task, selected owner route, target acceptance condition, supplied context, and whether the user explicitly authorized run-to recovery.
2. **Preflight required inputs**. Ask the selected owner to resolve current required artifacts, accepted inputs, readiness evidence, and producer routes before target mutation.
3. **Classify the result**. Execute a ready target normally, classify a missing input with an available in-scope producer as paused recovery, and reserve blocked status for an unavailable external state change. See **Status Classification**.
4. **Present recovery choices when authorization is absent**. Stop before prerequisite mutation, show the missing inputs and recommended dependency order, and offer the choices in **Recovery Choices**.
5. **Apply the selected recovery posture**. Execute only the next prerequisite when selected, return an alternate route for review, leave state unchanged on stop, or enter **Run-To Target** after explicit authorization.
6. **Run to the target when authorized**. Use the native planning tool to maintain the target closure, invoke each owner under its own contract, refresh durable state after every bounded result, and execute the original target when ready.
7. **Stop at protected boundaries**. Pause at every boundary in **Nondelegable Boundaries** and report the exact decision or state change needed to resume the same target.
8. **Return the target outcome**. Lead with whether the original target completed, paused, or blocked; summarize material prerequisite Runs and refs without turning each intermediate terminal report into another routine user prompt.

If the user's task does not map cleanly to these steps, use the native planning tool to build a target-scoped recovery plan from the selected owner, current durable state, producer routes, authorization, and boundaries in this reference, then execute the plan or pause at a protected boundary.

## Recovery Choices

When an ordinary `do <task>` request has producible missing prerequisites, present these semantic choices in natural language:

| Choice | Effect |
| --- | --- |
| Run to the target | Execute the recommended in-scope transitive prerequisites and then execute the original target. Mark this recommended when the closure is clear and safe. |
| Execute the next prerequisite only | Invoke the first recommended producer and return its outcome without silently continuing. |
| Inspect or choose another route | Explain material alternatives and let the user revise the recovery path. |
| Stop | Perform no prerequisite mutation and leave the target paused. |

Accept `run to <task>`, `automate the prerequisites and then do <task>`, `yes to all` after this prompt, and semantically equivalent explicit language as run-to authorization. An ordinary imperative request authorizes the target only; it does not authorize prerequisite mutation. When the original request already explicitly authorizes automatic prerequisites and names the target, begin run-to after preflight without repeating the choices.

## Run-To Target

Run-to is prompt-scoped controller authorization, not a new Isomer Control Mode, CLI command, Project setting, or session-wide preference. The internal plan ends at the original target and may add newly discovered routine, reversible, in-scope prerequisites without another prompt. It ends when the target completes, the user interrupts or changes the target, a protected boundary is reached, or the closure cannot make progress.

Preserve owner boundaries throughout the traversal. Each owner performs its own mutation, callbacks, validation, and durable recording. Keep separate Research Tasks, Runs, terminal reports, Artifacts, checkpoints, Gates, and provenance when their contracts require them. A bounded terminal report ends one owner invocation; during authorized run-to it does not automatically end the user-level target traversal.

Do not continue into later recommendations, cleanup, refactoring, publication, submission, or unrelated work after the target succeeds.

## Status Classification

Use `paused` when a missing or stale prerequisite has an available in-scope producer or repair owner. Report the exact input, producer route, recommended order, recovery choices, and target resume point.

Use `blocked` only when no available authorized owner can produce the required state and progress depends on an external state change. Report the external condition, affected target, and resume condition.

An invalid input may block its bounded consumer while still having a separate in-scope repair route. Without run-to authorization, pause and offer that route. With run-to authorization, invoke the repair owner separately and retry the consumer only after refreshing durable state.

## Nondelegable Boundaries

Pause before any required human Gate, material change to the requested goal, destructive or irreversible action, credentials or restricted data, material license decision, unexpected cost or resource use, public exposure, publication or submission, or choice whose alternatives materially change the task's meaning. Check every selected owner's own Gate and authorization rules; the original target request is not blanket approval.

When traversal repeats a recovery route without producing new accepted state, pause with the completed refs and repeated condition instead of looping.

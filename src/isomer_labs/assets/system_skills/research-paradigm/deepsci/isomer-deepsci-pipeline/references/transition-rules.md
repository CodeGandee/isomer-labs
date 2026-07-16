# Stage Transition Rules

When `isomer-deepsci-pipeline` finishes a stage, it applies these rules to decide whether to continue, pause, or stop.

## Continue

The pipeline proceeds to the next stage when all of the following are true:

- The stage completed without emitting a blocker record.
- The stage's route decision matches the continue condition given in the recipe table.
- The stage produced all artifacts listed in the next stage's `consumes` list.
- The caller has not sent an interrupt or stop signal.

## Pause

The pipeline pauses (status `paused`) when:

- The stage's route decision matches the pause condition given in the recipe table but is not a hard blocker.
- The stage recommends a user-sensitive decision before continuing.
- The stage's output indicates the recipe should hand off to a different skill or pipeline.
- A required input is missing or stale and a known in-scope focused skill or pass can produce or repair it.

The terminal report includes the stage id, the unexpected route, known producer, original target resume point, and all artifacts produced so far. The bounded recipe ends; it does not add a backward edge or invoke the producer internally.

## Block

The pipeline stops (status `blocked`) when:

- The stage emits a blocker record.
- A required artifact is invalid with no authorized repair owner, or its production depends on an unavailable external state change.
- The stage fails catastrophically and cannot produce a route decision.

The terminal report includes the blocker record and a `resume_point` pointing to the failed stage.

## Stop

The pipeline stops (status `complete`) when the terminal stage finishes successfully. The terminal report's `recommended_next` field is derived from the last stage's route decision.

## Controller Responsibilities

Without explicit run-to authorization, the external controller reports the missing input and offers run to the target, execute the next prerequisite only, inspect or choose another route, and stop. It does not mutate prerequisites from an ordinary target request.

After explicit target-scoped run-to authorization, the current agent acting as external controller may:

- Invoke the recommended focused skill or a different single-pass recipe as a separate Run.
- Validate its terminal report and refresh the latest context before the next invocation.
- Resume a paused recipe from the `resume_point`, or restart it when the recipe does not support that entry, after accepting the required input.
- Stop after the original target or at a nondelegable human Gate, material choice, destructive action, unexpected resource boundary, publication, submission, or external side effect.

The pipeline skill does not choose among these options.

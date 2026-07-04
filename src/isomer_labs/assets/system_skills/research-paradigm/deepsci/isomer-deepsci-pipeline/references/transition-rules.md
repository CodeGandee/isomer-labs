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

The terminal report includes the stage id, the unexpected route, and all artifacts produced so far.

## Block

The pipeline stops (status `blocked`) when:

- The stage emits a blocker record.
- A required artifact is missing or invalid.
- The stage fails catastrophically and cannot produce a route decision.

The terminal report includes the blocker record and a `resume_point` pointing to the failed stage.

## Stop

The pipeline stops (status `complete`) when the terminal stage finishes successfully. The terminal report's `recommended_next` field is derived from the last stage's route decision.

## Controller responsibilities

After receiving a terminal report, the external controller may:

- Run the same recipe again from the beginning.
- Run a different recipe.
- Resume a paused recipe from the `resume_point` after resolving the blocker or decision.
- Stop macro work entirely.

The pipeline skill does not choose among these options.

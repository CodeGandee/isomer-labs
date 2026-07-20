# Prerequisite Recovery

## Workflow

1. **Capture the requested target**. Preserve the original Kaoju intent or compatibility procedure, its accepted stop condition, and whether the user explicitly authorized run-to recovery.
2. **Preflight its prerequisites**. Resolve accepted Artifact refs, audit state, workspace readiness, bindings, producer procedures, and required Gates before beginning the target Run.
3. **Classify gaps**. A missing or stale input with a known in-scope producer yields `paused` prerequisite recovery. Use `blocked` only when progress needs an unavailable external state change.
4. **Prompt before prerequisite mutation**. For an ordinary target request, recommend the dependency path and offer Run to the target, Execute the next prerequisite only, Inspect or choose another route, and Stop.
5. **Plan an authorized closure**. After explicit target-scoped run-to authorization, use the native planning tool to track the transitive prerequisite procedures and the original target.
6. **Invoke bounded owners**. Give every procedure its own Run, callbacks, checkpoints, Gates, Artifact acceptance, and terminal report. Refresh durable state before selecting the next planned procedure.
7. **Pause at nondelegable boundaries**. Stop for required human Gates, material choices, destructive or irreversible actions, credentials or restricted data, license decisions, unexpected resources, public exposure, publication, or submission.
8. **Stop at the target**. Return the original target outcome and material prerequisite refs. Do not continue into later recommendations after the target succeeds.

If the task does not map cleanly to these steps, use the native planning tool to build a target-scoped dependency plan from current durable state, known producer routes, explicit authorization, and protected Gates, then execute it or pause at the first nondelegable boundary.

## Authorization Scope

An ordinary `do <task>` request authorizes only the named Kaoju target. It does not authorize acquisition, repair, audit, synthesis, drafting, build, or another prerequisite procedure that the target discovers.

Explicit `run to <target>`, `automate the prerequisites and then do <target>`, a `yes to all` answer to the recovery prompt, or equivalent language authorizes the routine in-scope prerequisite closure and the target. This authorization is prompt-scoped and target-scoped, not global, session-wide, a CLI flag, a Project setting, or a Run-level Control Mode.

## Controller and Procedure Boundary

The current agent acts as the prompt-level controller during authorized run-to traversal. A Kaoju command page remains a bounded procedure: it never selects or executes another macro procedure internally. Its terminal report closes that procedure and may recommend a producer or repair route. The controller may consume that route only after recording the terminal report, validating its refs, refreshing current state, and confirming that the route remains inside the authorized target closure.

Keep separate Research Tasks, procedure Runs, terminal reports, Gates, Service Requests, command requests, Artifacts, and Provenance Records. A prerequisite owner retains mutation authority; controller authorization never transfers that authority to the pipeline.

## Recovery Result

For `paused`, report the missing input, known producer, recommended dependency order, four recovery choices, and exact target resume point. For `blocked`, report the unavailable external state change and resume condition. During run-to, do not turn routine intermediate completion into another choice prompt, but always pause at a nondelegable boundary.

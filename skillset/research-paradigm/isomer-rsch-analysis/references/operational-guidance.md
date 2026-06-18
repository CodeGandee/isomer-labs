# Operational Guidance

Use this reference when the analysis route needs longer operational notes than the main control surface.

Provenance: see `provenance.md`. Source runtime calls are mapped to Isomer host surfaces or TBD placeholders.

## Artifact Tactics

Use a durable campaign Artifact when lineage, slice-level isolated state, review visibility, rebuttal traceability, writing traceability, or later replay matters. Even one extra experiment can be represented as a one-slice campaign when durable lineage matters.

If a campaign assigns slice work to specific Agent Workspaces or Workspace Runtime surfaces, run each slice in the assigned surface unless there is a concrete reason to switch. Record that reason as Provenance.

Isolate the campaign from the current Run, Research Inquiry Relationship, or result Artifact rather than mutating a completed parent in place when lineage matters. Only create or launch the campaign after verifying that listed slices are executable with the current assets and runtime, or after marking infeasible slices explicitly.

When the campaign is writing-facing, the campaign Artifact should carry available mapping fields such as selected outline ref, research questions, experimental designs, todo items, section ids, claim links, reviewer items, or target display ids when they exist and matter.

If ids or refs are unclear, recover them through host Artifact, Provenance, or Finding query surfaces instead of guessing. Use `[[tbd-surface:api-artifact-record]]` and `[[tbd-surface:api-finding-query]]` until those surfaces are settled.

Treat campaign ids as system-owned when a host system provides them. Treat slice ids or todo ids as agent-authored semantic ids unless the host contract says otherwise.

After each launched slice finishes, fails, or becomes infeasible, record the same durable truth immediately. A failed or infeasible slice still needs status, real blocker, evidence path if any, claim update, comparability verdict, and next recommendation.

For slice recording, deviations and evidence paths are context fields, not mandatory ceremony. Include them when they materially help explanation or auditability. A concise evaluation summary is the preferred stable routing summary for operator review, report work, review, and rebuttal.

Useful slice summary fields include:

- `takeaway`
- `claim_update`
- `baseline_relation`
- `comparability`
- `failure_mode`
- `next_action`

## Resource Gate

Before launching a multi-slice campaign or expensive slice, record the current execution envelope:

- available GPUs, CPUs, memory, and storage
- expected wall-clock budget
- concurrency or queue limits
- services, credentials, dependencies, or data access that may block execution

For each planned slice, decide explicitly:

- runnable as written
- runnable only after downscoping
- infeasible in the current environment

Do not keep an infeasible slice as if it were still on equal footing with runnable slices. Replace it with a lower-cost proxy, defer it with a blocker note, or drop it with rationale.

## Execution Tactics

Use the execution route that is most faithful, observable, and efficient while preserving the hard Gates.

- A bounded smoke test is useful when command shape, outputs, metric path, or evaluator wiring is uncertain.
- Treat smoke work as a small validation budget, not as a mandatory phase.
- If the path is already concrete, go straight to direct verification or the real slice.
- If two candidate slices answer the same evidence question, prefer the one that preserves the most soundness under the current hardware and time budget.
- If runtime is uncertain or long, use the host Execution Adapter in an observable mode and keep a monitoring plan.
- When logs are long, preserve enough beginning, ending, and targeted middle context to audit failures and progress.
- Track stall signals such as silence, progress age, signal age, or overdue watchdogs when the host exposes them.
- If a slice is invalid, wedged, or superseded, stop it through the host Execution Adapter and record why.
- When waiting on long work, prefer bounded waits followed by evidence inspection over open-ended waiting.
- When slice code is under agent control, prefer concise structured progress markers.
- If the same failure class appears again without route or evidence change, stop widening and route through decision.
- If the same slice repeatedly fails because the environment cannot support it, stop retrying and redesign the slice set around the real resource envelope.

Use `[[tbd-surface:api-execution-command]]` until command execution, monitoring, and logging behavior are settled.

## Durable Context Note

Use durable context only to avoid repeating known failures or to preserve reusable campaign lessons, not as a required step before every slice.

At stage start, query recent Findings when resuming, reopening old command paths, or prior campaign lessons are likely to matter. Run targeted Finding queries before launching or resuming slices when repeated failures, prior slice outcomes, or comparability caveats may affect the route.

At stage end, record a Finding when the campaign produced a reusable cross-slice lesson, failure pattern, or comparability caveat.

Use `[[tbd-surface:api-finding-query]]` until Finding query and write surfaces are settled.

## Operator-Facing Campaign Chart Notes

When a campaign result becomes an operator-facing or report-facing chart:

- use restrained palettes and stable chart conventions from the host figure skill or design system
- use color to separate campaign-critical slices from background slices, not to decorate every slice equally
- keep the main boundary change obvious in compact previews

Use figure output Artifacts resolved by Workspace Path Resolution for figure source and exports.

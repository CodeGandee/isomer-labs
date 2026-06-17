# Campaign Design

Use this reference when an analysis campaign exists to strengthen evidence
rather than to accumulate miscellaneous extra runs.

Provenance: see `provenance.md`. Source runtime terms have been mapped to
Isomer Artifacts, Evidence Items, Research Claims, Gates, Execution Adapter
surfaces, and TBD placeholders.

## Goal

A strong campaign should move the evidence boundary from:

- fragile to interpretable
- minimum to solid
- solid to broader confidence

It should do so with the highest soundness gain that still fits the current
execution envelope. Do not treat every available follow-up as equally valuable.

## Priority Order

Prefer this order:

1. claim-critical contradiction checks
2. strongest robustness or sensitivity checks
3. failure-mode explanation
4. efficiency or secondary support

Within the same priority tier, prefer the slice that is both runnable now and
most likely to change the Research Claim boundary.

## Analysis Routes

Use the lightest route that preserves trust and downstream utility:

- `analysis-lite`: one clear follow-up question, one slice or a very small
  slice set, and a compact durable result.
- `durable evidence package`: one or more slices that need durable lineage,
  isolated Agent Workspace or Workspace Runtime state, review visibility, or
  later replay.
- `writing-facing campaign`: evidence directly supports a selected outline,
  evidence ledger, section, claim, table, or report display.
- `review/rebuttal campaign`: evidence directly answers reviewer pressure or
  audit findings.
- `failure-analysis route`: evidence explains why a result failed, diverged, or
  became non-comparable.

Start with the smallest route that can answer the current follow-up question.
Run claim-critical slices first and stop widening once the next route is clear.

## Slice Classes

- `auxiliary`: helps understand settings, thresholds, or mechanisms, but does
  not carry the main claim by itself.
- `claim-carrying`: directly affects whether the main narrative or route
  decision is justified.
- `supporting`: broadens confidence or interpretability after the main claim is
  already credible.
- `failure-analysis`: explains failure class, non-comparability, or route
  invalidation.

## Writing-Facing Policy

If the campaign is tied to an outline, report, review, or rebuttal package:

- run claim-carrying slices first
- only then run supporting slices that deepen interpretation
- route back to write once the evidence is strong enough for the selected
  narrative
- keep `manuscript_takeaway` or report-facing takeaway separate from internal
  setup, operator instructions, command history, and provenance
- classify evidence as claim-carrying, supporting, auxiliary, comparator,
  negative, or reference-only

## Resource-Aware Design Gate

Before expanding a slice set, record the current practical limits:

- available machine class or devices
- expected wall-clock budget
- memory and storage limits
- concurrency limits
- environment, dependency, service, credential, or queue risk

Then tag each candidate slice as one of:

- `runnable-now`
- `runnable-with-downscope`
- `blocked-by-resources`

When resources are tight, optimize for soundness-per-cost:

- prefer one decisive runnable contradiction or robustness slice over several
  speculative expensive slices
- use narrower sweeps, fewer seeds, shorter horizons, smaller held-out subsets,
  or cheaper diagnostics when they still answer the question honestly
- record blocked high-value slices explicitly instead of letting them disappear

Use `[[tbd-surface:api-execution-command]]` for unsettled execution command
surfaces and `[[tbd-surface:path-analysis-output]]` for unsettled analysis
output layouts.

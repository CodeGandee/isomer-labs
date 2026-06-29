# Analysis Quantity and Operations

Analysis-campaign sizing targets, the full slice-evidence contract, and the longer campaign +
decision operational tactics.

Houmao adaptation: durable slice rows are written with `$HARNESS record apply` (legacy:
`artifact.record_analysis_slice(...)`); paper-contract reads use `$HARNESS state query` /
`runs/<quest-id>/paper/...` (`artifact.get_paper_contract(...)` /
`artifact.validate_manuscript_coverage(...)`); managed shell + monitoring is the harness shell.

## Paper-facing analysis quantity target

For manuscript-support campaigns, first audit the paper contract and, when a draft exists, the
manuscript-coverage validator.

- A mature empirical manuscript usually needs **5-10 ready paper-facing experiment/analysis
  groups total, with 4-8 reviewer-facing analysis jobs** in the outline when the paper is full
  empirical. Fewer is acceptable only for an early/narrow outline with an explicit waiver.
- If the user requested a concrete analysis count, such as **4-8 reviewer-facing analyses**,
  treat it as a tracked target; report the completed/mapped count and any explicit waiver before
  returning to full-paper writing.
- Do not pad the count with stale methods, abandoned methods, unrelated baseline repairs, or old
  exploratory rows. Each slice must identify the current method or claim it supports.
- If legacy-method analysis is intentionally included, mark it as baseline/comparator/negative
  evidence and keep it separate from current-method support.
- Paper-facing slice outputs must separate the `manuscript_takeaway` from internal setup, user
  instructions, worktree paths, command history, and artifact provenance.
- Do not encode local throughput shorthand such as `64 + 64` as a manuscript takeaway; record
  exact per-endpoint settings only as reproducibility/protocol detail when needed.
- If the count is below the needed range, create the smallest claim-critical frontier rather than
  pretending the manuscript is ready.

## Slice evidence contract

For each meaningful slice, define and record enough of the following to make the evidence
reusable:

- research question
- hypothesis, expected pattern, or decision-relevant expectation
- intervention, ablation, variation, inspection target, or failure bucket
- controls or fixed conditions
- metric, observable, table, qualitative artifact, or rubric
- comparison target
- expected resource class or major execution constraint when it affects feasibility
- stop condition or completion condition
- evidence path expectations
- claim update
- comparability verdict
- next action

Code-based, fully automatable analysis is preferred when it is the most faithful and repeatable
path. But not every valid analysis must be fully automatable: failure-bucket inspection,
qualitative artifact review, extracted-text audits, reviewer-linked example checks, or
table/figure consistency checks can be valid when the evidence is concrete, sampled or scoped,
and reproducible enough for the claim being made. Do not present subjective judgment as objective
measurement; if human/model/qualitative judgment is used, record the rubric, sample, prompt or
inspection basis, caveats, and why it is sufficient for the route decision.

## Slice classes

- `auxiliary`: helps understand settings, thresholds, or mechanisms but does not carry the main
  claim by itself
- `claim-carrying`: directly affects whether the main narrative or route decision is justified
- `supporting`: broadens confidence or interpretability after the main claim is already credible

## Campaign artifact tactics

Use an artifact-backed campaign when durable lineage or slice-level branch/worktree state
matters. Even one extra experiment can be represented as a one-slice campaign when durable
lineage matters, when the slice should appear as a real child node in Git/Canvas, or when review,
rebuttal, or paper traceability benefits from the campaign object.

- If the campaign creation returns slice worktrees, run each returned slice in its returned
  workspace unless there is a concrete reason to switch, and record that reason.
- Branch the campaign from the current workspace or result node rather than mutating the
  completed parent node in place when lineage matters.
- Only create the campaign after verifying the listed slices are executable with the current
  quest assets and runtime, or explicitly mark infeasible slices as such.
- When writing-facing, carry available paper-mapping fields such as `selected_outline_ref`,
  `research_questions`, `experimental_designs`, and `todo_items` when they exist and matter.
- If ids or refs are unclear, recover them first (resolve runtime refs / read the campaign /
  read quest state / list outlines) instead of guessing. Treat `campaign_id` as system-owned, and
  treat `slice_id` / `todo_id` as agent-authored semantic ids.
- After each launched slice finishes, fails, or becomes infeasible, record the same durable truth
  immediately. If a slice fails or becomes infeasible, still record an honest non-success status
  plus the real blocker and next recommendation; do not leave the campaign state ambiguous.
- `deviations` and `evidence_paths` are context fields, not mandatory ceremony; include them when
  they materially help explanation or auditability. An `evaluation_summary` is the preferred
  stable routing summary for UI, Canvas, review, and rebuttal; when useful include `takeaway`,
  `claim_update`, `baseline_relation`, `comparability`, `failure_mode`, `next_action`.

## Resource gate

Before launching a multi-slice campaign or any expensive slice, record the current execution
envelope in the durable route record: available GPUs, CPUs, memory, and storage; expected
wall-clock budget; concurrency or queue limits; services, credentials, or dependencies that may
block execution. For each planned slice, decide explicitly: `runnable as written`; `runnable
only after downscoping`; `infeasible in the current environment`. Do not keep an infeasible slice
as if it were on equal footing with runnable slices — replace it with a lower-cost proxy, defer
it with a blocker note, or drop it.

## Execution and monitoring tactics

Use whatever execution route is most faithful, observable, and efficient while preserving the
hard gates. These tactics describe the managed harness shell:

- a bounded smoke test is useful when the slice command, outputs, metric path, or evaluator
  wiring is uncertain; treat smoke work as a `0-2` default budget, not a mandatory phase
- if the path is already concrete, go straight to direct verification or the real slice
- if two candidate slices answer the same evidence question, prefer the one that preserves the
  most soundness under the current hardware and time budget
- if runtime is uncertain or likely long, prefer a detached run plus managed monitoring
- a managed-log read returns the full rendered log when it is 2000 lines or fewer; for longer
  logs it returns the first 500 lines plus the last 1500 lines, and you can inspect omitted
  middle sections with explicit start/tail
- monitor newest-first; after the first read, prefer incremental reads keyed on the last seen
  sequence so later checks only fetch new evidence; recover ids from the session history if they
  become unclear
- use stall checks such as `silent_seconds`, `progress_age_seconds`, `signal_age_seconds`, and
  `watchdog_overdue` when available
- if a slice is invalid, wedged, or superseded, kill it explicitly and relaunch cleanly
- for pure wall-clock waiting between checks, use a bounded await and do not set the timeout
  exactly equal to the sleep length; prefer awaiting an already-running session over starting a
  fresh sleep
- when you control the slice code, prefer a throttled progress reporter and concise structured
  progress markers
- if the same failure class appears again without a real route or evidence change, stop widening
  the campaign and route through `decision`; if the same slice repeatedly fails because the
  environment cannot support it, stop retrying and redesign the slice set around the real
  resource envelope

## Slice recording discipline

Record slice-level evidence before making any campaign-level claim. Every meaningful slice should
leave a durable outcome (completed, partial, failed, blocked, infeasible, or superseded) and a
claim update. Null, negative, failed, partial, and contradictory findings must remain visible.
Campaign-level interpretation must be derived from per-slice evidence rather than impressions. If
two slices in a row fail to change the claim boundary, matrix frontier, or next route, stop
widening and route through `decision`, `write`, `experiment`, or an explicit blocker.

## Checkpoint-memory resume card (route decisions)

When a route decision materially changes the authoritative resume point, write one compact
checkpoint-style quest memory card (`type:checkpoint-memory`). The card should
include: current active node; node history; what not to reopen by default; first files to read.
In Houmao the authoritative resume state lives in `runs/<quest-id>/...` files plus the DB; the
memory card is advisory continuity context.

## Connector-facing campaign chart notes

When a campaign result is promoted into a connector-facing chart: prefer restrained palettes such
as `sage-clay` (a useful anchor is `#7F8F84`) and `mist-stone`; use color to separate
campaign-critical slices from background slices rather than decorating every slice equally; keep
the palette consistent with the system prompt instead of improvising a fresh theme per campaign;
make the main boundary change obvious even in compressed connector previews.

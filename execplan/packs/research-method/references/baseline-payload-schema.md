# Baseline Payload Schema

Advisory schema documentation for the accepted-baseline payload and the verification verdicts.
md`. This is reference craft, **not** a DB schema
definition — the canonical baseline gate in Houmao is set with
`$HARNESS record apply --type quest.update --baseline_gate passed|waived|blocked`
(`artifact.confirm_baseline(...)` / `artifact.waive_baseline(...)`). Use this
file to shape the payload you record; do not modify the DB schema to match it.

For the compact verdict rubric, also read `references/comparability-contract.md`.

## Accepted-baseline payload shape

The accepted baseline artifact should include at least:

- `baseline_id`
- `baseline_kind`
- `path`
- `task`
- `dataset`
- `primary_metric`
- `metrics_summary`
- `environment`
- `source`
- `summary`

(persisted contract additionally tracks per-metric `derivation` / `origin_path`
/ `source_ref`; see the metric-contract rules below.)

## Metric-contract rules

- keep `primary_metric` as the headline metric only; do not let it erase the rest of the
  comparison surface
- submit canonical `metrics_summary` as a **flat top-level dictionary keyed by the paper-facing
  metric ids**
- every canonical baseline metric entry should include `description`, either `derivation` or
  `origin_path`, and `source_ref`
- mark only the currently required canonical metrics as required; additional metrics can be
  added later or kept supplementary
- if the accepted baseline contract already needs multiple metrics, datasets, subtasks, or
  splits, record them in the canonical metric-contract file
  (`<baseline_root>/json/metric_contract.json`)
- if the paper reports both aggregate and per-dataset or per-task results, preserve both
  whenever feasible through `metrics_summary` plus structured rows rather than one cherry-picked
  scalar
- if the source package already has a richer leaderboard table, structured result file, or
  metric-contract json, reuse that richer contract instead of hand-writing a thinner one that
  keeps only one averaged scalar
- `Result/metric.md` is optional temporary scratch memory only; reconcile against it before
  setting the baseline gate, but do not treat it as a required durable file

The core metric contract makes the comparison explicit: task identity; dataset identity and
split contract; evaluation script or path; required metric keys for the current downstream
comparison; metric directions; source commit or source-package identity; known deviations from
the source reference. A core contract is enough to confirm a `comparison_ready` baseline; expand
it later when paper claims, registry publication, or variant-heavy comparison need more coverage.

## Verification verdicts

Verification is mandatory before baseline acceptance. Classify the outcome as exactly one of:

- `verified_match` — the run/service-call/package-import/trusted-output inspection finished, the
  reported metrics came from the intended dataset and split, metric definitions and directions
  match the quest contract, and the result reproduces the comparator within tight agreement.
- `verified_close` (`close`) — the result is comparable to the paper / source repo / local
  comparator / registry package / selected target within expected stochastic variance or a small
  explained gap, rather than an exact match.
- `verified_diverged` (`diverged`) — the run completed and is traceable, but the result departs
  materially from the expected comparator value and the divergence is not yet explained away as
  variance; the gap is real and recorded.
- `trusted_with_caveats` — the comparator is usable downstream, but only with explicitly recorded
  caveats (e.g. an environment mismatch, a documented protocol deviation, or a partial metric
  surface) that later stages must carry forward.
- `broken` — verification failed: outputs cannot be tied to the intended command/source/service,
  the run failed before producing evidence, or the metrics are not traceable. The baseline gate
  must not be opened; record the blocker and next route instead.

Verification should explicitly separate likely implementation mismatch, environment mismatch,
data or split mismatch, expected stochastic variance, and unexplained divergence when those
distinctions matter.

# Analysis Campaign Boundary Cases

Use this reference when the evidence route is plausible but the success boundary, comparability boundary, or stage boundary is still fuzzy. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Check whether this is actually a new main experiment**. Route back to experiment or idea when the proposed change defines a new main method, replaces the comparison target, or would become the new primary measured line.
2. **Label useful non-comparable slices**. Keep stress tests, different metric families, altered protocols, and limitation-boundary checks useful but separate from direct comparison support.
3. **Validate qualitative evidence**. Use qualitative or reviewer-example evidence only with a concrete sample, rubric or inspection basis, trace, and caveat.
4. **Stop after one decisive slice**. End the campaign when one slice clarifies the claim boundary and extra slices add polish rather than route-changing information.
5. **Stop repeated no-evidence failure loops**. Record a blocker, redesign, return to experiment, or route through decision when the same failure class repeats without new route, evidence, or environment change.
6. **Separate pre-outline from paper-ready analysis**. Run pre-outline analysis when it determines whether writing is worthwhile, and require <ANALYSIS_WRITEBACK_MAP> before calling a slice paper-ready.
7. **Keep extra comparators local**. Use extra comparator evidence only as analysis-local support unless a separate route changes the canonical comparator basis.
8. **Separate support, contradiction, and ambiguity**. Do not blur stable support, contradiction, and unresolved ambiguity into one optimistic summary.

## Preferences

- Prefer routing to experiment when the slice would become a new primary measured line (if it is a bounded follow-up, otherwise keep it in analysis).
- Prefer explicit non-comparable labels over discarding useful stress-test evidence (if the slice is still decision-relevant, otherwise drop it).
- Prefer one decisive slice over a padded campaign (if the next route is clear, otherwise stop).
- Prefer blocker records over repeated failed retries (if failure repeats without new information, otherwise redesign).

## Constraints

- Analysis must not disguise a new main experiment.
- Non-comparable evidence must not be mixed into direct comparison tables as if it were apples-to-apples support.
- Subjective inspection must not be presented as objective measurement.
- Extra comparator evidence must not overwrite the canonical comparator basis.
- A paper-ready label must not be used without a write-back target.

## Quality Gates

### Metrics

- Boundary-label coverage: fraction of plausible boundary cases labeled as main experiment, non-comparable, qualitative, one-slice-sufficient, repeated failure, pre-outline, extra comparator, support, contradiction, or ambiguity; higher is better.
- Silent-widening count: number of repeated-failure or one-slice-sufficient cases that keep widening without blocker, redesign, route, or stop decision; lower is better.

### Checks

- Stage gate: the work is truly follow-up analysis rather than a new main experiment, baseline recovery, or idea revision.
- Comparability gate: direct, non-comparable, stress-test, limitation-boundary, or failure-analysis status is labeled.
- Qualitative gate: rubric, sample, inspection basis, trace, caveat, and route relevance are recorded.
- Stop gate: repeated failure and one-slice sufficiency cases route instead of widening silently.
- Interpretation gate: stable support, contradiction, and unresolved ambiguity are separate in <ANALYSIS_CAMPAIGN_SUMMARY>.

## Boundary Cases

- New-main-experiment case: route back to experiment or idea when the proposed slice changes the main method or comparison target.
- Non-comparable-but-useful case: keep external-validity, stress-test, altered-protocol, or limitation evidence separate from direct comparator support.
- Qualitative-evidence case: use concrete scoped samples and explicit rubrics; do not pretend subjective inspection is a benchmark metric.
- One-slice-enough case: stop when the parent boundary and next route are already clear.
- Repeated-failure case: record blocker or redesign when repeated failures add no evidence.
- Writing-facing pre-outline case: run the evidence check before writing only when it decides whether writing is worthwhile.
- Extra-comparator case: record local comparator support without overwriting the canonical comparator basis.
- Interpretation-boundary case: label stable support, contradiction, and ambiguity separately.

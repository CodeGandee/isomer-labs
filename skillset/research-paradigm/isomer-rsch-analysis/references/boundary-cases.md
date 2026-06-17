# Analysis Campaign Boundary Cases

Use this reference when the evidence route is plausible but the success boundary, comparability boundary, or stage boundary is still fuzzy.

Provenance: see `provenance.md`.

## 1. This Is Really a New Main Experiment

Do not hide a new main experiment inside analysis when:

- the proposed change defines a new main method
- the comparison target itself is being replaced
- the result would become the new primary measured line rather than a follow-up check

Route back to experiment or idea instead.

## 2. Non-Comparable but Still Useful

A slice can still be useful when it is not apples-to-apples comparable.

Examples:

- external dataset stress test
- different metric family used only for failure analysis
- altered protocol used to expose a limitation boundary

Required behavior:

- label the slice as non-comparable
- do not mix it into the main comparison table as if it were direct support

## 3. Qualitative or Reviewer-Example Evidence

This can be valid when:

- the claim is about failure buckets, behavior, or explanation
- the sample is concrete and scoped
- the rubric or inspection basis is explicit
- the evidence is used honestly as supporting or boundary evidence

This is not valid when subjective inspection is presented as if it were a benchmark metric.

## 4. One Slice Is Enough

Stop after one slice when:

- the claim boundary is already clear
- the next route is obvious
- extra slices would only add polish, not change the decision

Do not widen the campaign just because more follow-ups are imaginable.

## 5. Repeated Failure with No New Evidence

Stop widening when:

- the same failure class appears again
- no route changed
- no evidence changed
- no execution environment changed

At that point, record the blocker, redesign the slice, route through decision, or return to experiment.

## 6. Writing-Facing but Pre-Outline

This can still be legitimate when:

- the evidence question determines whether writing is even worth pursuing
- no paper-ready claim is being finalized yet

This becomes writing-ready only after it is mapped back to outline, evidence ledger, report matrix, section, claim, table, reviewer item, or rebuttal Artifact.

## 7. Extra Comparator Baseline Inside Analysis

This is allowed when:

- a slice genuinely needs an extra comparator
- that comparator is analysis-local support rather than the accepted baseline

Required behavior:

- keep the accepted baseline Gate unchanged
- record the extra comparator through comparison-baseline evidence fields

## 8. Stable Support vs Contradiction vs Ambiguity

Use these meanings:

- stable support: slice materially strengthens the parent claim
- contradiction: slice materially weakens or breaks the parent claim
- unresolved ambiguity: slice leaves the decision unclear

Do not blur these together in one optimistic summary.

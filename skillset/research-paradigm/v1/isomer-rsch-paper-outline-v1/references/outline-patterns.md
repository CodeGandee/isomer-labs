# Outline Patterns

Use these patterns when repairing an outline that is too close to implementation notes, run logs, or result dumps.

## Pattern: Small Mechanism, Big Lesson

Use when the method is simple but the result suggests a reusable principle. Instead of "we add a guard and rerun evidence collection", frame the paper around a principle such as separating evidence acquisition from guarded update. Needed analyses might include guard removed, extra evidence without guard, guard with no extra evidence, failure cases where the guard rejects changes, and budget sensitivity.

## Pattern: Targeted Repair

Use when aggregate gains are modest but a diagnosed subset improves. Instead of treating the result as weak because only a subset improves, frame it as targeted evidence repair. Needed analyses might define the deficient subset, compare gains inside and outside the subset, show examples of repaired cases, show residual failures, and compare with a stronger or simpler repair baseline.

## Pattern: Measurement Reframing

Use when the contribution is mostly how to measure or select data, evidence, or quality. Instead of "we compute many scores and report which one correlates best", frame the paper around the measure that predicts downstream generalization under matched scale and quality. Needed analyses might include controlled comparisons, ranking stability, old-measure failure cases, proxy sensitivity, and downstream result using the measure.

## Negative Examples

Bad: "The paper uses a selected outline, local branch, and exact execution route." Better: "The paper uses a fixed comparison budget on a held-out benchmark."

Bad: "The abstract states local endpoints and batch arithmetic." Better: "Exact local serving settings are appendix reproducibility details."

Bad: "The method is the latest operator requirement." Better: "The method is described as an evidence-acquisition and guarded-update procedure."

Bad: "The analysis plan has two runs because those are completed." Better: "The analysis plan is chosen from reviewer questions: cause, robustness, stronger baselines, failure modes, and cost."

## Quick Checklist

- Would a reader remember the one-sentence idea?
- Can every claim point to an Evidence Item?
- Does the outline say where each claim stops?
- Would the analysis plan answer likely reviewer questions?
- Can the paper-facing text appear in a manuscript without explaining local process?

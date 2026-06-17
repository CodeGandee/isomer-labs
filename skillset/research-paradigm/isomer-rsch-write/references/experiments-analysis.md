# Experiments and Analysis

Use this reference when strengthening experiments and analysis sections.

## Separate Proof from Interpretation

`Experiments` establishes where the method works, against whom, and under which settings. `Analysis` explains why the pattern is credible, what tradeoff it reveals, and where the claim boundary lies. Do not let analysis become a short epilogue after a result dump.

## Reviewer Questions

A strong experiments section answers explicit reviewer questions: Does the method beat named baselines on the main task? Does the gain persist across datasets, scales, or settings? Does the gain survive stronger baselines, retuning, or ablations? What practical cost, latency, or data tradeoff accompanies the gain?

## Comparison Surface

Keep the principal benchmark comparison and the relevant baseline families visible in main text when the central claim is comparative. Do not rely on prose claims that mention wins without a visible comparison surface. Do not collapse named competitors into self-only rows while retaining broad comparative wording.

## Display Roles

Useful experiment display jobs include headline benchmark, robustness or transfer, ablation or intervention, practical cost, and qualitative support. Useful analysis display jobs include mechanism check, credibility check, tradeoff or sensitivity check, failure boundary, and category breakdown.

## Analysis Evidence Floor

When the evidence package supports it, keep at least one mechanism or credibility display and one tradeoff, sensitivity, robustness, or quality-support display in main text. Compact displays are acceptable when they answer different reviewer concerns.

## Appendix Bridges

Bridge overflow evidence deliberately. Name the appendix job: extra benchmark slices, protocol details, broader sweeps, qualitative examples, annotation details, additional failure cases, full tables, or reproducibility detail.

## Fast Audit

Before stabilizing these sections, ask whether a reviewer can inspect the main comparative claim, whether non-headline robustness or objection-handling evidence is visible when needed, whether analysis names a stable pattern or mechanism, and whether main text carries enough evidence instead of outsourcing the entire analysis layer to appendix.

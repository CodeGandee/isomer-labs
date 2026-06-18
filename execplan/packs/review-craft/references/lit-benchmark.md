# Paper-quality literature benchmark

Houmao's `lit audit` only counts reference rows + reference-backed claims against a floor. This procedure
is the qualitative positioning audit that decides whether a gap is a *writing* fix or a *missing-evidence*
fix — run it during review, before requesting any new experiment.

## Build a comparator set of 3–8 papers
- 1–3 closest technical neighbors
- 1–3 writing / story exemplars (top-venue accepted papers: ICLR/ICML/NeurIPS/CVPR/ACL/EMNLP/Nature/Science/Q1)
- 1–2 experiment-package exemplars

Record (via `lit fetch` → `reference.record`, then `claim link`): title / venue / relevance + what each
teaches about abstract framing, problem→gap→method→evidence logic, reader onboarding, experiment
design/ablations/baselines, figure/table roles, related-work positioning.

## Novelty / related-work matrix
`Topic | This paper | Closest prior work | Overlap | Residual novelty/value` — forces genuine positioning
against the *nearest neighbors*, not the broad method family.

## Critical discipline
Do NOT request new experiments just to answer a literature-positioning question. First decide whether the
fix is writing, positioning, claim narrowing, or genuinely missing evidence. Citation floor for a mature
empirical paper trends well above the harness `min_refs` default — aim for real, claim-linked positioning
references, not a padded bibliography (see `execplan/docs/publication-quality.md`).

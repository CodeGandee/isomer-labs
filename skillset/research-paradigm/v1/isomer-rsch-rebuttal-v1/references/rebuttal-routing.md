# Rebuttal Routing

Use this reference when a reviewer item needs work outside the rebuttal packet itself.

## Route Table

| Reviewer pressure | Route |
| --- | --- |
| Explanation, organization, claim wording, response text, figure caption, or manuscript delta | `isomer-rsch-write-v1` |
| Novelty, related-work, positioning, or scope comparison | `isomer-rsch-scout-v1` |
| Missing or untrusted comparator baseline | `isomer-rsch-baseline-v1` |
| Reviewer-linked ablation, robustness check, error analysis, failure boundary, evidence repackaging, or supplementary run | `isomer-rsch-analysis-v1` |
| New or revised figure quality after data exists | `isomer-rsch-figure-polish-v1` or `isomer-rsch-paper-plot-v1` |
| Cost, deadline, claim downgrade, response stance, baseline recovery, or scope choice is non-trivial | `isomer-rsch-decision-v1` |
| Final revised manuscript package is ready after all feasible critical items resolve | `isomer-rsch-finalize-v1` |

## Supplementary Evidence Rules

Do not launch free-floating work. Every reviewer-linked evidence slice must name the reviewer item ids it answers, the hypothesis, required metric or observable, minimal success criterion, expected manuscript impact, and fallback wording if incomplete.

## Literature and Novelty

When a complaint is mainly about novelty, related work, or scope, run a focused literature or positioning audit before treating it as an experiment request.

## Baseline Recovery

When a reviewer requests a comparator that is missing or untrusted, route to baseline before analysis. If the response must proceed without an accepted active comparator, require a Baseline-Waiver Policy ref and any required Gate or Decision Record. Do not let a reviewer-linked analysis compare against an unfair or stale baseline.

## Closure

Do not treat the rebuttal package as final while reviewer-critical feasible rows remain pending. If a row cannot be fully addressed, record the limitation, downgrade the claim if needed, and explain the honest response.

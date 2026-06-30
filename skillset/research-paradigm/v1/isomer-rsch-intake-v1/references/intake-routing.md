# Intake Routing

Use this reference after state audit and trust ranking to choose the smallest valid handoff.

## Typical Intake States

- baseline-ready: a comparator is accepted and can support idea, experiment, analysis, writing, or finalization.
- baseline-partial: a comparator exists but needs verification, repair, acceptance, waiver, or replacement.
- main-result-ready: an accepted Run exists and needs analysis, writing, decision, or finalization.
- analysis-ready: follow-up evidence exists or is needed to update a Research Claim.
- draft-ready: writing Artifacts exist and need write, review, rebuttal, paper-outline, or finalize routing.
- paper-bundle-ready: a paper-like package exists and needs coverage, review, proofing, rebuttal, or closure.
- review-package-ready: reviewer comments or review outputs define the next task.
- unclear-state: durable state is too conflicting or thin to choose a stage without a Gate, repair, or decision.

## Handoff Choices

| Condition | Recommended handoff |
| --- | --- |
| Existing baseline is useful but not trusted | `isomer-rsch-baseline-v1` |
| Accepted baseline and selected route lack a durable main Run | `isomer-rsch-experiment-v1` |
| Main result exists but claim boundary is weak | `isomer-rsch-analysis-v1` |
| Evidence is strong enough for drafting or report repair | `isomer-rsch-write-v1` |
| Draft, outline, or paper package needs skeptical audit | `isomer-rsch-review-v1` |
| Reviewer comments define the task | `isomer-rsch-rebuttal-v1` |
| Several next stages remain plausible | `isomer-rsch-decision-v1` |
| Closure, pause, archive, or publication handoff is plausible | `isomer-rsch-finalize-v1` |
| Objective, metric, benchmark, or baseline neighborhood is still unclear | `isomer-rsch-scout-v1` |

## Gate Rules

Run Gate Policy preflight when the next route depends on scope, cost, credential use, privacy, safety, publication-facing output, finality, external upload, or a human-held source, and open or recommend a Gate when the selected policy requires Operator Agent judgment. Do not use a Gate for routine technical ambiguity that durable evidence can resolve.

## Route Decision Minimum

The route record should name the chosen handoff, decisive evidence, rejected alternatives, remaining verification, and what should not be repeated. If the concrete Decision Record schema matters, use the accepted Decision Record fields.

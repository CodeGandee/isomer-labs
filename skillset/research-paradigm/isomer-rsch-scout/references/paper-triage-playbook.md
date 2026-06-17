# Paper Triage Playbook

Use this reference when scout needs a more explicit process for building the smallest paper, repo, and benchmark neighborhood that can change the next route.

## Search Objective

Map only enough of the neighborhood to justify the task frame, evaluation contract, and baseline shortlist. The goal is not to collect many papers.

## Reuse Before Search

Before broad external search, inspect durable Findings, prior literature notes, task documents, accepted baselines, benchmark hints, and local Artifacts. Search only for missing pieces that affect baseline or idea routing.

## Search Order

1. Direct neighborhood: same task, dataset, benchmark, split, and metric.
2. Contract neighborhood: official benchmark docs, evaluation scripts, challenge pages, and official repos.
3. Baseline neighborhood: direct comparator papers, official repos, maintained implementations, and strong reproduced variants.
4. Mechanism neighborhood: same core mechanism, bottleneck, objective, architecture, data regime, or failure mode.
5. Provenance checks: web or repository checks only when source, version, or implementation trust remains unclear.

## Retain or Reject References

Retain a reference only when it informs task framing, evaluation contract, baseline route, later ideation, or a blocker. Reject references that are adjacent but do not change the next stage.

For each retained item, record title or identifier, source URL or Artifact id, year when known, why it matters, the question it informs, provenance label, and any caveat.

## Repository Triage

For a candidate implementation, inspect whether the repository is official or clearly linked, whether the evaluation path is obvious, whether dependencies are realistic, whether the metric and split match, and whether maintenance status affects trust.

## Stop Rules

Stop when the strongest obvious local neighbors are mapped, metric and split ambiguity no longer block route choice, and at least one baseline route is clearly better than the alternatives. Continue only when the current shortlist is too weak, conflicting, or missing provenance.

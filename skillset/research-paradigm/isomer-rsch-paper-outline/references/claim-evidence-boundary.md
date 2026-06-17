# Claim-Evidence Boundary

Use this reference when deciding what can become paper text.

## Observed Facts

Observed facts are directly visible in durable Evidence Items, validated outputs, logs, tables, figures, source documents, or verified code and configuration. They can support claims when their scope and caveats are explicit.

## Allowed Interpretations

Allowed interpretations are careful lessons supported by observed facts. They must state the evidence zone where they hold and what could weaken them.

## Must Not Claim

Must-not-claim items include unsupported generalization, unverified implementation behavior, baseline dominance not shown by evidence, citations not checked, future work not completed, and process facts disguised as scientific contribution.

## Paper View Versus Evidence View

Paper view should contain the reader-facing idea, scoped claims, method abstraction, evaluation plan, and analysis plan. Evidence view should contain exact runs, settings, metrics, source locations, reproducibility details, caveats, unmapped items, and local process facts that should not enter the narrative.

## Falsification Boundary

Every core claim should name a result pattern that would weaken or falsify it. This prevents the outline from becoming unfalsifiable story polish.

## Route Decisions

If a claim lacks evidence, route to `isomer-rsch-analysis` or downgrade the claim. If novelty or positioning is uncertain, route to `isomer-rsch-scout`. If a comparator is missing, route to `isomer-rsch-baseline`. If scope choice is non-trivial, route to `isomer-rsch-decision`.

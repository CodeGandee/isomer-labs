# Survey Quality Profile

Survey-paper quality is a multidimensional profile with explicit populations, exclusions, cutoffs, source refs, thresholds, and per-dimension verdicts. It is not a single opaque score.

## Dimensions

| Dimension | Measurements | Interpretation Boundary |
| --- | --- | --- |
| Protocol and scope coverage | Required scope cells covered, planned discovery channels executed, screening dispositions recorded, inclusion/exclusion accounting, temporal cutoff, bounded discovery-saturation trend | Measures execution against the Survey Contract, not completeness of an unknowable literature universe |
| Source identity integrity | Canonical identity and version posture, unresolved identities, duplicate/variant collapses, inaccessible-source accounting | Counts unresolved identity as uncertainty; prevents variants from inflating coverage |
| Evidence adequacy | Claims meeting required verification depth, exact-locator coverage, primary-source use where required, unresolved blockers | Keeps source-stated, source-supported, executed, compared, contradicted, and inconclusive evidence distinct |
| Comparative-study soundness | Operational dimensions, comparability status, matched-depth comparisons, missing/non-comparable cells, normalization, fairness, asymmetry | A large matrix is not sound when methods were checked at different depths or under incompatible conditions |
| Traceability | Claims, citations, tables, figures mapped to accepted records and locators; citation keys and bibliography resolved | A reviewer can audit each conclusion and display |
| Synthesis quality | Survey questions answered, taxonomy categories with boundary cases, contradictions and negative findings represented, gaps distinguished from missing search, calibrated conclusions | Rewards useful organization without inventing consensus or novelty |
| Balance and limitations | Material source-class, venue, time, provider, geographic, or method-family skews reported; audited limitations propagated | Reports observed imbalance and blind spots rather than hiding them behind aggregate counts |
| Reader-facing reporting | Section jobs distinct, tables and figures state question and takeaway, terminology consistent, methods reproducible, main-text detail separated from appendices | Judges understandability and reviewability, not promotional tone |
| Document integrity | Numbering, citations, hierarchy, extracted text, layout, readability, accessibility, build provenance, file integrity | Publication readiness still requires the separate rendered-document checks |

## Verdicts

Each applicable dimension receives one of:
- `pass`
- `warning`
- `fail`
- `not-applicable`
- `unknown`

A mandatory `fail` or `unknown` produces `not-ready`. Warnings require authorization defined by the paper contract and applicable Gate. A composite score, when explicitly defined, cannot override a mandatory failed or unknown dimension.

## Reporting Rules

- Every measure names its numerator, denominator or bounded population, exclusions, unknown cases, and accepted source records.
- Discovery saturation and source counts are bounded observations, not proof that the literature universe is complete.
- Unknown denominators remain visible.

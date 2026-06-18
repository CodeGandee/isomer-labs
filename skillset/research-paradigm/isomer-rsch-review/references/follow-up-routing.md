# Follow-up Routing

Use this reference after the audit identifies serious issues.

## Route Table

| Finding | Route |
| --- | --- |
| Text, outline, figure-caption, claim-scope, or framing issue with enough evidence | `isomer-rsch-write` |
| Novelty, positioning, or related-work uncertainty | `isomer-rsch-scout` |
| Missing or untrusted comparator baseline | `isomer-rsch-baseline`, or `isomer-rsch-decision` when a Baseline-Waiver Policy-backed waiver and Gate are needed |
| Concrete evidence gap, ablation, robustness check, error analysis, failure analysis, or evidence mapping issue | `isomer-rsch-analysis` |
| Figure/table quality weakness after the underlying data exists | `isomer-rsch-figure-polish` or `isomer-rsch-paper-plot` |
| Concrete reviewer comments requiring point-by-point response | `isomer-rsch-rebuttal` |
| Non-trivial route, cost, claim downgrade, stop, Research Inquiry Relationship, or publication-scope choice | `isomer-rsch-decision` |
| Manuscript is truly ready after review and Gates pass | `isomer-rsch-finalize` |

## Follow-up Gates

If the review scope is audit-only, stop after durable review artifacts and a route recommendation. If the next expensive step triggers Gate Policy preflight, package one structured Gate when Operator Agent judgment is required. If follow-up execution already has a resolved Gate or policy clearance and the route is clear, proceed through the routed skill rather than leaving the review as a dead end.

## Blocker Types

Separate analysis blockers, manuscript blockers, language/provenance blockers, citation blockers, submission blockers, and user-decision blockers. This prevents review from converting every problem into "run more experiments."

# Citation and Bibliography Guidance

Use this reference when writing depends on literature support, reference counts, BibTeX quality, related-work positioning, or citation truth.

## Citation Truth

Do not hand-write citations, BibTeX entries, venues, dates, metrics, or related-work claims from recollection. Treat bibliography facts as Evidence Items that must come from a verified paper source, DOI or arXiv metadata, proceedings page, journal page, or another accepted literature capability. If the provider is not settled, mark the dependency with `[[tbd-surface:provider-literature-search]]`.

## Search Pattern

Use breadth, shortlist, depth. Breadth finds candidate papers and families. Shortlist chooses the papers that directly affect claims, novelty boundaries, or section framing. Depth reads the papers that the manuscript cites, compares against, or uses as exemplars.

## Bibliography Expectations

For paper-like deliverables, aim for enough verified references to support the claimed scope. A full empirical manuscript often needs a broad enough bibliography to cover closest neighbors, method family, evaluation setting, datasets or benchmarks, and positioning claims. A small report or checkpoint can justify fewer, but every citation must still be real and relevant.

## BibTeX Hygiene

Keep bibliography entries machine-usable and consistent with manuscript citations. Check that keys are stable, titles and venues are accurate, duplicate entries are removed, author lists are not malformed, and cited entries appear in the bibliography. Do not claim a bibliography check was run unless it was executed through an approved Execution Adapter.

## Related-Work Discipline

Position related work by closest-neighbor boundary, not by bibliography volume. Distinguish similar goal, similar mechanism, similar evaluation setting, and direct comparator. Do not attack prior work merely to make the current line look novel. If novelty or closest-neighbor status is uncertain, route to `isomer-rsch-scout` before drafting strong claims.

## Citation Gaps

Citation gaps are not always evidence gaps. If the issue is positioning, use literature search and manuscript revision. If a cited comparison requires a missing benchmark or metric, route to `isomer-rsch-baseline` or `isomer-rsch-analysis`.

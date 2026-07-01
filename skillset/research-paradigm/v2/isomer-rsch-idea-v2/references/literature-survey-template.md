# Literature Survey Report Template

Use this template at the start of a fresh idea pass and whenever an existing candidate needs deeper refinement. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Write the survey header**. Identify the Research Topic, date, comparator basis, task, dataset, metric contract, current investigation target, and survey minimum gate status.
2. **Record prior evidence first**. List Workspace Runtime records, prior paper notes, idea notes, decision notes, and reusable knowledge consulted before external search.
3. **Maintain a search ledger**. For every meaningful search pass, record the query, source, reason, newly added papers, reconfirmed known papers, and remaining gap.
4. **Bucket the papers**. Split evidence into core papers, closest competitors, adjacent inspirations, cross-domain transferable mechanisms, and watchlist items.
5. **Build the closest-prior-work table**. Compare mechanism, task, dataset, metric, supported claim, weakness, and implication for each serious candidate.
6. **State novelty and value verdicts**. Label serious candidates as `novel`, `incremental but valuable`, or `not sufficiently differentiated`.
7. **Translate to code and memory**. Record implementation levers, feasibility blockers, cheapest falsification paths, and <IDEA_MEMORY_RECORD> writes to create or refresh.
8. **Prepare citation support**. Extract the papers that must support <SELECTED_IDEA_DRAFT> before final selection.

## Preferences

- Prefer reusing recent durable survey coverage before external search (if the coverage is stale or incomplete, otherwise search only the missing buckets).
- Prefer standard citation entries for papers that shape the selected idea (if citation style is not specified, otherwise use one consistent style).
- Prefer paper buckets over a flat bibliography (if the paper only checks novelty, otherwise mark it separately from direct support).

## Constraints

- <LITERATURE_SURVEY_REPORT> must separate reused findings, newly retrieved papers, unresolved gaps, and watchlist items.
- <LITERATURE_SURVEY_REPORT> must include a search ledger for meaningful search passes.
- Paper-ready promotion must not proceed without closest-prior-work comparison and citation-ready support.
- The selected route must not claim novelty from recall alone.

## Quality Gates

### Metrics

- Usable related-paper count: number of related and usable papers covered by the survey; higher is better until at least 5 and usually 5-10 papers are covered.
- Paper-bucket coverage: number of required paper buckets represented across core papers, closest competitors, adjacent inspirations, cross-domain transferable mechanisms, and watchlist items; higher is better.
- Unresolved search-gap count: number of route-relevant gaps still open after meaningful search passes; lower is better.

### Checks

- Coverage gate: the survey durably covers at least five and usually five to ten usable related papers for paper-ready selection, or explicitly documents why fewer exist.
- Ledger gate: every new external query closes a named gap rather than restarting broad discovery from zero.
- Novelty gate: every serious candidate has a closest-prior-work verdict.
- Citation gate: <SELECTED_IDEA_DRAFT> can cite the papers that shaped the mechanism, motivation, novelty check, or claim boundary.

# Literature Survey

Use this reference at the start of a fresh idea pass and whenever an existing idea needs deeper refinement. The purpose is to make related-work coverage durable, searchable, and reusable so later turns do not repeat the same broad search.

## Survey Header

- Research Task or Research Inquiry Relationship id.
- Date.
- Comparator id or method name.
- Task, dataset, and metric contract.
- Current investigation target.
- Survey minimum gate status: related usable papers, direct task papers, adjacent translatable papers, cross-domain mechanism papers, and whether the usable-paper floor is satisfied.
- Why the survey is being run now: first idea build, idea refinement, novelty check after failure, or update for newer papers.

## Durable Context Consulted Before External Search

List Findings, Evidence Items, Artifacts, Decision Records, prior paper notes, idea notes, and knowledge cards checked before new search. Record what they covered well and what gaps remained.

## Search Ledger

| Query | Capability | Reason | New papers | Known papers reconfirmed | Remaining gap |
| --- | --- | --- | --- | --- | --- |
| baseline plus limitation keyword | Literature Provider Binding ref | find direct extensions; record provider output as a provider-output Artifact before deriving Findings or Evidence Items | | | |

## Paper Buckets

- Core papers.
- Closest competitors.
- Adjacent inspirations.
- Cross-domain transferable mechanisms.
- Watchlist or uncertain relevance.

For each paper, include title, year, identifier or URL, citation string or key, mechanism summary, task overlap, dataset overlap, metric overlap, provider-output Artifact ref when externally sourced, implication for the candidate, and status as new, known, or watchlist.

## Closest-Prior-Work Table

| Identifier | Year | Citation key | Mechanism overlap | Task overlap | Dataset overlap | Metric overlap | Strongest supported claim | Weakness or unresolved edge | Implication |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Novelty and Value Verdict

For each serious candidate, state the closest prior art, mechanism overlap, what remains missing, and verdict: `novel`, `incremental but valuable`, or `not sufficiently differentiated`.

## Codebase Translation Note

Connect the literature back to the current implementation surface: relevant modules, required implementation levers, likely feasibility blockers, and cheapest falsification path. Use semantic Artifact kind through Workspace Path Resolution rather than inventing repository-specific output paths.

## Citation-Ready Shortlist

Before final idea selection, extract the papers that materially support the winning idea. For each paper, record the standard citation entry, whether it supports problem motivation, closest prior work, mechanism inspiration, or claim boundary, and whether it must appear inline in the final idea draft.

## Exit Rule

The selected route should not be promoted until the survey separates reused prior coverage, newly added comparisons, and still-missing overlaps.

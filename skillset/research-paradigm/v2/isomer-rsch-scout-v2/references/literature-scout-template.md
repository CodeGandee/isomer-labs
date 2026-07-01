# Literature Scouting Report Template

Use this template when external discovery materially changes the research frame, evaluation contract, comparator shortlist, or next route. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Confirm report necessity**. Write `<LITERATURE_SCOUTING_REPORT>` only when discovery changed or justified routing.
2. **Fill from route evidence**. Use `<SCOUT_CONTEXT_BRIEF>`, `<SCOUT_MINIMUM_UNKNOWNS>`, `<SCOUT_DISCOVERY_LEDGER>`, `<EVALUATION_CONTRACT>`, and `<BASELINE_SHORTLIST>`.
3. **Maintain a search ledger**. Record query or inspection, source surface, reason, new references, reconfirmed references, and unresolved ambiguity.
4. **Bucket retained references**. Separate task-defining papers, benchmark docs, candidate comparator papers, candidate comparator repositories, and watchlist or rejected references.
5. **State route implications**. Summarize evaluation-contract implications, baseline-shortlist implications, and `<NEXT_ROUTE_DECISION>`.
6. **Link continuity**. Mention `<SCOUT_CONTINUITY_UPDATE>` so future baseline or idea work can reuse the report.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer retained references that change routing over long paper summaries (if a reference is only adjacent, otherwise put it in watchlist or reject).
- Prefer provenance labels such as official, community, or uncertain (if provenance is unclear, otherwise treat it as a route risk).
- Prefer one next-route recommendation over open-ended literature commentary.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- `<LITERATURE_SCOUTING_REPORT>` must include a search ledger when external discovery affects routing.
- The report must separate retained, watchlist, and rejected references when that distinction prevents downstream rework.
- The report must state how discovery changed `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, `<NEXT_ROUTE_DECISION>`, or `<SCOUT_BLOCKER_RECORD>`.
- Scout must not write a literature report just to collect references after the next route is already clear.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Discovery-gap closure: number of search passes that close a named task, metric, baseline, provenance, or split gap; higher is better.
- Route-relevant reference count: number of retained references that affect task framing, evaluation contract, baseline shortlist, or next anchor; higher is better until route clarity is reached.

### Checks

- Reuse value: the report prevents later baseline or idea work from restarting the same discovery.
- Route impact: every retained reference explains which task, evaluation, comparator, or future-idea question it informs.
- Provenance clarity: official, community, and uncertain sources are distinguishable.
- Exit clarity: the report ends with a justified route or blocker.

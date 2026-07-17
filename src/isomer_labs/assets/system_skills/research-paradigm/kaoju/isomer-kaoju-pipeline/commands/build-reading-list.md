# Build Reading List

## Workflow

1. Resolve one accepted direction and its independent direction scope. Never merge several selected directions into one implicit list.
2. Resolve the target request before discovery. With no count, target three priority and three secondary works. For category counts, use each supplied non-negative integer and default an omitted category to three. For one positive total `N`, target `(N + 1) // 2` priority and `N // 2` secondary works. Ask for clarification before discovery when the request mixes total and category modes, uses invalid counts, or produces an empty target.
3. Search across papers, technical reports, repositories, datasets, and models while treating papers and reports as primary works. Record query or seed, provider or access method, route, searched-through date, identity resolution, version family, disposition, and coverage limits in the Discovery Ledger.
4. Reach the effective priority and secondary targets. Preserve inaccessible or unresolved targets as blockers; use bounded backfill without hiding shortages.
5. Deduplicate versions by work family while retaining exact version identities and relationships.
6. Present the list for inspection and refinement. Report the effective and achieved category counts. A short list may be approved with a non-blocking shortage warning against the effective target.
7. Persist `KAOJU:READING-LIST` as a scoped current-state Artifact with `target_counts` and `achieved_counts`, then checkpoint the Run. Record the target basis as `default`, `user-total`, or `user-categories`, and record `requested_total` for `user-total`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-discover`. Inputs: accepted `KAOJU:DIRECTION-SET`, direction id, Survey Contract, provider bindings, and optional target-count request. Outputs: scoped Reading List and Discovery Ledger refs.

## Gates, Blockers, and Resume

Human approval is required. Provider failure, source-access limits, unresolved identity, or binding failure records blockers. Resume at discovery, backfill, refine, or approve without discarding prior query provenance.

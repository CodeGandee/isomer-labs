# Build Reading List

## Workflow

1. Resolve one accepted direction and its independent direction scope. Never merge several selected directions into one implicit list.
2. Search across papers, technical reports, repositories, datasets, and models while treating papers and reports as primary works. Record query or seed, provider or access method, route, searched-through date, identity resolution, version family, disposition, and coverage limits in the Discovery Ledger.
3. Target three reachable priority works and three reachable secondary works. Preserve inaccessible or unresolved targets as blockers; use bounded backfill without hiding shortages.
4. Deduplicate versions by work family while retaining exact version identities and relationships.
5. Present the list for inspection and refinement. A short list may be approved with a non-blocking shortage warning.
6. Persist `KAOJU:READING-LIST` as a scoped current-state Artifact and checkpoint the Run.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this command, its required inputs, and the user's request, then execute the plan.

## Owner, Inputs, and Outputs

Owner: `$isomer-kaoju-discover`. Inputs: accepted `KAOJU:DIRECTION-SET`, direction id, Survey Contract, provider bindings. Outputs: scoped Reading List and Discovery Ledger refs.

## Gates, Blockers, and Resume

Human approval is required. Provider failure, source-access limits, unresolved identity, or binding failure records blockers. Resume at discovery, backfill, refine, or approve without discarding prior query provenance.

# Operational Guidance

Use this reference when a scout pass needs more than a short clarification step. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Confirm scout is needed**. Check whether existing context already yields `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, and `<NEXT_ROUTE_DECISION>`.
2. **Reconstruct `<SCOUT_CONTEXT_BRIEF>`**. Summarize the current Research Topic or Research Inquiry, task boundary, dataset and split understanding, metric direction, comparator status, and blockers.
3. **Reuse prior knowledge**. Build `<SCOUT_MEMORY_REUSE_NOTE>` from Workspace Runtime context, Artifact summaries, Finding summaries, Decision Record summaries, and compatibility memory retrieval before broad discovery.
4. **Classify `<SCOUT_MINIMUM_UNKNOWNS>`**. Keep only unknowns that block baseline work, idea work, both, a Gate, a Decision Record, or an explicit blocker.
5. **Resolve route-changing unknowns only**. Use local evidence first, then the smallest useful paper, repository, benchmark, or provenance discovery surface.
6. **Create route-facing outputs**. Draft `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, and `<LITERATURE_SCOUTING_REPORT>` only to the extent needed for downstream routing.
7. **Choose the next route**. Record `<NEXT_ROUTE_DECISION>` for baseline, idea, decision, Gate, blocker, or another justified v2 route.
8. **Record continuity**. Preserve `<SCOUT_CONTINUITY_UPDATE>` when scout changes the frame, records a blocker, or produces a reusable literature, comparator, or metric lesson.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer quick exit when the frame is already explicit and the next route is obvious (if not, otherwise continue with the minimum unknowns).
- Prefer local durable context and Workspace Runtime records before new discovery (if local evidence is insufficient, otherwise search only the missing neighborhood).
- Prefer conclusion-first scout outputs over large documentation packages (if external discovery changed the route, otherwise write the smallest durable report that prevents rework).
- Prefer `isomer-rsch-baseline-v2` unless a comparator is already durable and trustworthy enough for `isomer-rsch-idea-v2`.
- Prefer stopping on clarity over searching to exhaustion.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Scout must not become endless exploration.
- Scout must not ask routine technical questions before checking local durable evidence.
- Scout must not guess metric, split, comparator identity, or evaluation contract when evidence is ambiguous.
- Scout must not repeat the same broad discovery when prior Artifacts, Findings, Decision Records, or Workspace Runtime notes already narrow the space.
- Scout must not write long paper summaries that do not change `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, `<NEXT_ROUTE_DECISION>`, or `<SCOUT_BLOCKER_RECORD>`.
- Scout must search for disconfirming evidence, not only supportive evidence.
- Scout must record a blocked state when required source evidence, evaluation choice, or comparator viability remains unresolved.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Unresolved routing unknown count: number of framing unknowns that still change baseline, idea, decision, Gate, or blocker routing; lower is better.
- Retained discovery relevance: fraction of retained discoveries that change frame, evaluation contract, comparator shortlist, or next route; higher is better.

### Checks

- Entry fit: scout runs only when framing ambiguity blocks routing, and exits when routing is already clear.
- Context quality: `<SCOUT_CONTEXT_BRIEF>` states current task, dataset, split, metric, comparator status, evidence already available, and blockers.
- Unknown quality: `<SCOUT_MINIMUM_UNKNOWNS>` contains only questions that can change baseline, idea, decision, Gate, or blocker routing.
- Discovery quality: `<SCOUT_DISCOVERY_LEDGER>` is limited to retained evidence that changes the frame, evaluation contract, comparator shortlist, or next route.
- Output quality: `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, `<LITERATURE_SCOUTING_REPORT>`, and `<NEXT_ROUTE_DECISION>` are just detailed enough for the next route.
- Blocker quality: `<SCOUT_BLOCKER_RECORD>` names what is missing, why it matters, which route is blocked, and what user choice or source is needed.

## Compatibility Harness

Use Workspace Runtime, Artifact, Literature Provider Binding, repository inspection, and Execution Adapter Command Request surfaces when available. When a source-compatible call is still the only binding, route it through `isomer-cli ext deepsci call <namespace.tool> --input-json <json-object>` and status the durable meaning with the placeholders in `../migrate/placeholders.md`.

# Operational Guidance

Use this reference when a scout pass needs more than a short clarification step. Placeholder definitions live in `../migrate/placeholders.md`.

## Workflow

When this reference is used, execute the following steps in order.

1. **Confirm scout is needed**. Check whether existing context already yields `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, and `<NEXT_ROUTE_DECISION>`.
2. **Reconstruct `<SCOUT_CONTEXT_BRIEF>`**. Summarize the current Research Topic or Research Inquiry, task boundary, dataset and split understanding, metric direction, comparator status, and blockers.
3. **Reuse prior knowledge**. Create `<SCOUT_MEMORY_REUSE_NOTE>` from Workspace Runtime, Artifacts, Findings, Decision Records, and compatibility memory retrieval before broad discovery.
4. **Classify `<SCOUT_MINIMUM_UNKNOWNS>`**. Keep only unknowns that block baseline work, idea work, both, a Gate, a Decision Record, or an explicit blocker.
5. **Resolve only route-changing unknowns**. Use local evidence first, then the smallest useful paper, repository, benchmark, or provenance discovery surface.
6. **Create route-facing outputs**. Draft `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, and `<LITERATURE_SCOUTING_REPORT>` only to the extent needed for downstream routing.
7. **Choose the next route**. Record `<NEXT_ROUTE_DECISION>` for baseline, idea, decision, Gate, blocker, or another justified v2 route.
8. **Record continuity**. Preserve `<SCOUT_CONTINUITY_UPDATE>` when scout changes the frame, records a blocker, or produces a reusable literature, comparator, or metric lesson.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this reference, the scout entrypoint, and the available evidence, then execute the plan.

## Current Frame

`<SCOUT_CONTEXT_BRIEF>` should be conclusion-first and compact:

- Current Research Topic or Research Inquiry.
- Bounded Research Task the user appears to need.
- Dataset, benchmark, split, and metric understanding.
- Known comparator or baseline status.
- Evidence already available as Artifacts, Evidence Items, Findings, Decision Records, or repository docs.
- Blockers that make route selection unsafe.

If this brief is already precise enough, scout may stop after recording `<NEXT_ROUTE_DECISION>`.

## Prior Knowledge Reuse

Before broad discovery, inspect local durable state and then retrieve relevant prior knowledge. When a DeepScientist-compatible memory surface is still the only available binding, use `isomer-cli ext deepsci call memory.list_recent --input-json <json-object>` and `isomer-cli ext deepsci call memory.search --input-json <json-object>`.

Search terms should target the current task, benchmark, dataset, split, metric, likely comparator names, official repository names, and paper identifiers. Summarize useful results in `<SCOUT_MEMORY_REUSE_NOTE>` rather than copying raw retrieval output into the scout result.

## Unknown Classification

Classify each item in `<SCOUT_MINIMUM_UNKNOWNS>` as one of:

- Blocks `isomer-rsch-baseline-v2`.
- Blocks `isomer-rsch-idea-v2`.
- Blocks both baseline and idea work.
- Requires `isomer-rsch-decision-v2` or a Gate.
- Useful later but non-blocking now.

Drop non-blocking curiosity from the scout critical path. Scout should resolve the smallest set of unknowns that changes routing.

## Discovery Ladder

Use this ladder only after local evidence and prior knowledge leave route-changing unknowns:

1. Direct neighborhood: same task, dataset, benchmark, split, and metric.
2. Mechanism neighborhood: same main method lever, objective, architecture, or optimization idea.
3. Bottleneck neighborhood: same failure mode, evaluation caveat, reproducibility issue, or boundary condition.

Prefer primary papers, official benchmark docs, official repositories, and maintained reusable code over secondary summaries. If a specific paper needs reading, use a Literature Provider Binding or a DeepScientist-compatible artifact extension call; use full-text retrieval only when the shorter provider result cannot answer the route-changing question.

## Evaluation Contract

`<EVALUATION_CONTRACT>` should state:

- Task.
- Dataset or benchmark.
- Split or evaluation partition.
- Primary metric and direction.
- Secondary metrics only when they affect routing.
- Fair-comparison rule.
- Useful-improvement threshold.
- Evidence and known ambiguity.
- Decision impact.

If two plausible contracts would change conclusions, stop with `<SCOUT_BLOCKER_RECORD>` or route to `isomer-rsch-decision-v2` instead of guessing.

## Baseline Shortlist

`<BASELINE_SHORTLIST>` should be small and decision-facing. For each serious comparator candidate, score provenance, metric and split compatibility, implementation availability, environment risk, expected cost, downstream comparison value, and recommended route: attach, import, reproduce, or reject.

Recommend one route at the end. Prefer `isomer-rsch-baseline-v2` unless a comparator is already durable and trustworthy enough for `isomer-rsch-idea-v2`.

## Continuity

When scout changes the frame, preserve the durable meaning as `<SCOUT_CONTINUITY_UPDATE>`. This may reference updated Artifacts, Findings, Decision Records, Gates, compatibility memory writes, or other Workspace Runtime records once storage binding exists.

When a DeepScientist-compatible memory write is still needed, call it through `isomer-cli ext deepsci call memory.write --input-json <json-object>` and summarize the durable result rather than binding future readers to the raw call payload.

## Blocked State

Create `<SCOUT_BLOCKER_RECORD>` when scouting cannot proceed responsibly because:

- The Research Topic, Research Inquiry, or expected task is materially ambiguous.
- Required paper, code, benchmark, dataset, or repository evidence is missing.
- Multiple evaluation contracts conflict and the choice would change later conclusions.
- Comparator candidates are too weak, broken, stale, or poorly specified.

The blocker must state what is missing, why it matters, which route is blocked, and what concrete user choice or source is needed.

## Stop Rules

Stop discovery when:

- The strongest local neighbors are mapped.
- Evaluation no longer depends on unknown source evidence.
- At least one comparator route is clearly better than the alternatives.
- Additional papers or repositories no longer change `<NEXT_ROUTE_DECISION>`.

Continue only when metric, split, provenance, or comparator ambiguity still changes downstream routing.

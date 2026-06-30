# Paper Triage Playbook

Use this reference when scout must map a paper, repository, benchmark, or provenance neighborhood before routing. Placeholder definitions live in `../migrate/placeholders.md`.

## Workflow

When this playbook is used, execute the following steps in order.

1. **Set the triage question**. Name the route-changing uncertainty from `<SCOUT_MINIMUM_UNKNOWNS>`.
2. **Reuse local evidence**. Check `<SCOUT_CONTEXT_BRIEF>` and `<SCOUT_MEMORY_REUSE_NOTE>` before external discovery.
3. **Search the smallest useful neighborhood**. Build `<SCOUT_DISCOVERY_LEDGER>` around direct, mechanism, and bottleneck neighbors.
4. **Retain only route-changing references**. Keep papers, repositories, and benchmark docs that affect task framing, `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, or `<NEXT_ROUTE_DECISION>`.
5. **Inspect repository provenance when needed**. Check official linkage, evaluation path, dependency realism, maintenance signal, and reproducibility risk.
6. **Stop on routing clarity**. Convert retained evidence into `<LITERATURE_SCOUTING_REPORT>`, `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, or `<SCOUT_BLOCKER_RECORD>`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step triage plan from the scout entrypoint, the route-changing uncertainty, and available provider surfaces, then execute the plan.

## Search Objective

The goal is not to collect many papers. The goal is to map the smallest neighborhood that can justify the task frame, evaluation contract, comparator shortlist, or blocker.

## Search Order

Use this order unless the user provides a more specific source:

1. Existing Artifacts, Evidence Items, Findings, Decision Records, repository docs, and `<SCOUT_MEMORY_REUSE_NOTE>`.
2. Primary papers and official benchmark documentation for the direct task, dataset, split, and metric.
3. Official repositories and clearly linked implementation repositories.
4. Mechanism-neighbor papers that share the main method lever or objective.
5. Bottleneck-neighbor papers that explain failures, evaluation caveats, or boundary conditions.
6. Broader web or repository search for provenance checks, recency checks, and missing links.

When a provider-bound paper route is available, prefer that route for paper discovery and only read full text when the route-changing detail is absent from summary metadata.

## Retention Test

Retain a reference only when it answers at least one question:

- Does it define or clarify the task?
- Does it define the benchmark, dataset, split, metric, or fair-comparison rule?
- Does it supply, reject, or rank a comparator candidate?
- Does it change whether baseline or idea should be next?
- Does it reveal a blocker or risk that must be recorded?

Reject references that are merely adjacent, duplicative, or unlikely to change downstream work. Mention rejected references only when their rejection prevents future rework.

## Repository Triage

For a candidate repository, inspect:

- Whether the repository is official or clearly linked from the paper, benchmark, organization, or maintainer.
- Whether the evaluation path maps to `<EVALUATION_CONTRACT>`.
- Whether dependencies and runtime assumptions look realistic for the Topic Workspace.
- Whether the code appears maintained or at least stable enough for attach, import, or reproduce work.
- Whether license, data, model weights, or benchmark access could block use.

Fold repository findings into `<SCOUT_DISCOVERY_LEDGER>` and `<BASELINE_SHORTLIST>` rather than producing a broad repository audit.

## Stop Condition

Stop triage when retained references are enough to rank comparator routes, settle metric and split ambiguity, or record a blocker. Continue only if remaining ambiguity would change `<NEXT_ROUTE_DECISION>`.

# Evaluation Contract Template

Use this when scout must make task, dataset, split, metric, fairness, evidence, or ambiguity explicit before routing. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Collect evidence**. Start from `<SCOUT_CONTEXT_BRIEF>`, `<SCOUT_MEMORY_REUSE_NOTE>`, `<SCOUT_DISCOVERY_LEDGER>`, user constraints, Workspace Runtime records, Artifacts, Evidence Items, Findings, Decision Records, literature sources, benchmark docs, and repository sources.
2. **State the contract**. Fill the task, dataset or benchmark, version or source, split, official evaluation path, primary metric, metric direction, secondary metrics, useful-improvement threshold, and fair-comparison rule.
3. **Name ambiguity honestly**. If two contracts conflict and would change downstream conclusions, record `<SCOUT_BLOCKER_RECORD>` or route to `isomer-rsch-decision-v2`.
4. **Connect downstream use**. State which downstream skill needs the contract and why.
5. **Stop at sufficient clarity**. Do not turn the contract into a full benchmark report unless routing depends on that detail.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer official benchmark docs, official repositories, primary papers, and local durable evidence over recollection (if they conflict, otherwise record the conflict).
- Prefer a concise route-facing contract over a long benchmark survey (if detail does not change routing, otherwise leave it out).
- Prefer routing to decision over guessing when metric, split, or fairness conflicts would change later conclusions.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- `<EVALUATION_CONTRACT>` must state task, dataset, split, metric direction, fair-comparison rule, useful-improvement threshold, evidence, known ambiguities, and decision impact when those fields affect routing.
- Scout must not guess metric, split, or comparator identity when local evidence is ambiguous.
- Baseline, idea, experiment, analysis, decision, or Gate routing must not proceed from conflicting evaluation contracts.
- Remaining ambiguity must be recorded rather than hidden.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Evaluation-contract field coverage: fraction of task, dataset, split, primary metric, metric direction, fair-comparison rule, useful-improvement threshold, evidence, and ambiguity fields completed; higher is better.
- Remaining ambiguity count: number of evaluation-contract ambiguities that still change baseline, idea, experiment, or blocker routing; lower is better.

### Checks

- Downstream sufficiency: `isomer-rsch-baseline-v2`, `isomer-rsch-idea-v2`, and `isomer-rsch-experiment-v2` can use the contract without re-deriving task, split, metric, or fairness.
- Evidence traceability: key contract fields cite local, literature, benchmark, or repository evidence.
- Ambiguity visibility: unresolved ambiguity is tabled with impact and proposed resolution.
- Route impact: the contract explains why it is sufficient now or why it blocks routing.

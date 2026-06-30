# Evaluation Contract Template

Use this template when scout must make task, dataset, split, metric, fairness, evidence, or ambiguity explicit before routing. Placeholder definitions live in `../migrate/placeholders.md`.

## Workflow

When this template is used, execute the following steps in order.

1. **Collect evidence**. Start from `<SCOUT_CONTEXT_BRIEF>`, `<SCOUT_MEMORY_REUSE_NOTE>`, and `<SCOUT_DISCOVERY_LEDGER>`.
2. **State the contract**. Fill every field in `<EVALUATION_CONTRACT>` that affects baseline, idea, experiment, analysis, decision, or Gate routing.
3. **Name ambiguity honestly**. If two contracts conflict and would change conclusions, record `<SCOUT_BLOCKER_RECORD>` or route to `isomer-rsch-decision-v2`.
4. **Connect downstream use**. State which downstream skill needs the contract and why.
5. **Stop at sufficient clarity**. Do not turn the contract into a full benchmark report unless the route depends on that detail.

If the user's task does not map cleanly to these steps, use your native planning tool to build an evaluation-contract plan from the available evidence and route question, then execute the plan.

## Template

```md
# Evaluation Contract

## Scope

- Research Topic:
- Research Inquiry or Research Task:
- Task:
- Dataset or benchmark:
- Dataset version or source:
- Split or evaluation partition:
- Official or expected evaluation path:

## Metrics

- Primary metric:
- Metric direction:
- Secondary metrics:
- Useful-improvement threshold:
- Known statistical or reporting caveats:

## Fair Comparison

- Comparator class:
- Fair-comparison rule:
- Accepted deviations:
- Disallowed comparisons:
- Required ablations or controls:

## Evidence

- User constraints:
- Artifacts or Evidence Items:
- Findings:
- Decision Records:
- Literature or benchmark sources:
- Repository sources:
- Discovery ledger: <SCOUT_DISCOVERY_LEDGER>

## Known Ambiguities

| Ambiguity | Why It Matters | Blocks | Proposed Resolution |
| --- | --- | --- | --- |
|  |  | baseline, idea, experiment, analysis, decision, Gate |  |

## Decision Impact

- Downstream route affected:
- Why this contract is sufficient now:
- Remaining risk:
- Output placeholder: <EVALUATION_CONTRACT>
```

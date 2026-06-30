# Baseline Shortlist Template

Use this template when scout must recommend a concrete comparator route before baseline or idea work can proceed. Placeholder definitions live in `../migrate/placeholders.md`.

## Workflow

When this template is used, execute the following steps in order.

1. **Start from the evaluation contract**. Use `<EVALUATION_CONTRACT>` to decide which comparator candidates are relevant.
2. **Gather candidate evidence**. Use `<SCOUT_DISCOVERY_LEDGER>`, `<LITERATURE_SCOUTING_REPORT>`, repository inspection, and existing Artifacts or Findings.
3. **Score serious candidates only**. Keep the shortlist small and score candidates by provenance, metric and split fit, implementation availability, environment risk, expected cost, downstream value, and main risk.
4. **Assign a route per candidate**. Choose attach, import, reproduce, or reject.
5. **Recommend one next action**. End with `<NEXT_ROUTE_DECISION>` and record `<SCOUT_BLOCKER_RECORD>` if no candidate is responsible to use.

If the user's task does not map cleanly to these steps, use your native planning tool to build a comparator-shortlist plan from the evaluation contract and candidate evidence, then execute the plan.

## Template

```md
# Baseline Shortlist

## Contract Basis

- Evaluation contract: <EVALUATION_CONTRACT>
- Research Topic:
- Research Inquiry or Research Task:
- Comparator need:

## Candidate 1

- Name:
- Source paper or repository:
- Candidate role: direct baseline, strong competitor, adjacent reference, sanity check
- Route: attach, import, reproduce, reject
- Provenance trust: high, medium, low
- Metric and split match:
- Implementation availability:
- Environment risk:
- Expected cost:
- Downstream value:
- Why it matters:
- Main risk:
- Evidence refs:

## Candidate 2

- Name:
- Source paper or repository:
- Candidate role:
- Route:
- Provenance trust:
- Metric and split match:
- Implementation availability:
- Environment risk:
- Expected cost:
- Downstream value:
- Why it matters:
- Main risk:
- Evidence refs:

## Ranking

| Candidate | Route | Trust | Fit | Cost | Value | Main Risk | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | attach, import, reproduce, reject | high, medium, low | high, medium, low | low, medium, high | high, medium, low |  |  |

## Recommendation

- Recommended candidate:
- Recommended route:
- Why this route now:
- Fallback route:
- Blocker if none is usable: <SCOUT_BLOCKER_RECORD>
- Output placeholder: <BASELINE_SHORTLIST>
- Next route: <NEXT_ROUTE_DECISION>
```

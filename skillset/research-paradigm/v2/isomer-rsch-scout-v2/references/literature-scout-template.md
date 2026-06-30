# Literature Scouting Report Template

Use this template when external discovery materially changes the research frame, evaluation contract, comparator shortlist, or next route. Placeholder definitions live in `../migrate/placeholders.md`.

## Workflow

When this template is used, execute the following steps in order.

1. **Confirm report necessity**. Write `<LITERATURE_SCOUTING_REPORT>` only when discovery changed or justified routing.
2. **Fill the report from evidence**. Use `<SCOUT_CONTEXT_BRIEF>`, `<SCOUT_MINIMUM_UNKNOWNS>`, `<SCOUT_DISCOVERY_LEDGER>`, `<EVALUATION_CONTRACT>`, and `<BASELINE_SHORTLIST>`.
3. **Separate retained and rejected references**. Keep only references whose inclusion or rejection prevents downstream rework.
4. **State route impact**. End with `<NEXT_ROUTE_DECISION>` or `<SCOUT_BLOCKER_RECORD>`.
5. **Link continuity**. Mention the expected `<SCOUT_CONTINUITY_UPDATE>` so future baseline or idea work can reuse the report.

If the user's task does not map cleanly to these steps, use your native planning tool to build a report plan from the discovery ledger and route decision, then execute the plan.

## Template

```md
# Literature Scouting Report

## Survey Header

- Research Topic:
- Research Inquiry or Research Task:
- Date:
- Why scouting was needed:
- Route-changing unknowns: <SCOUT_MINIMUM_UNKNOWNS>

## Search Ledger

| Query or Inspection | Source Surface | Reason | New References | Reconfirmed References | Unresolved Ambiguity |
| --- | --- | --- | --- | --- | --- |
|  | Literature Provider Binding, official repo, benchmark doc, repository inspection, open web, compatibility artifact call |  |  |  |  |

## Reference Buckets

### Task-Defining Papers

| Reference | Identifier or URL | Year | Provenance | Why It Matters | Informs |
| --- | --- | --- | --- | --- | --- |
|  |  |  | official, community, uncertain |  | task framing, evaluation contract, baseline route, future ideation |

### Benchmark and Evaluation Docs

| Reference | Identifier or URL | Provenance | Contract Impact | Remaining Ambiguity |
| --- | --- | --- | --- | --- |
|  |  | official, community, uncertain |  |  |

### Candidate Comparator Papers

| Reference | Identifier or URL | Year | Comparator Role | Route Impact |
| --- | --- | --- | --- | --- |
|  |  |  | direct baseline, strong competitor, adjacent reference | attach, import, reproduce, reject, watch |

### Candidate Comparator Repositories

| Repository | URL | Linkage | Evaluation Path | Implementation Risk | Route Impact |
| --- | --- | --- | --- | --- | --- |
|  |  | official, linked, community, uncertain |  |  |  |

### Watchlist or Rejected References

| Reference | Reason Kept or Rejected | Future Trigger |
| --- | --- | --- |
|  |  |  |

## Evaluation-Contract Implications

- Task:
- Dataset or benchmark:
- Split:
- Primary metric and direction:
- Fair-comparison rule:
- Useful-improvement threshold:
- Still-open ambiguity:
- Output placeholder: <EVALUATION_CONTRACT>

## Baseline-Shortlist Implications

| Candidate | Paper Evidence | Repository Evidence | Provenance Confidence | Recommended Route | Main Risk |
| --- | --- | --- | --- | --- | --- |
|  |  |  | high, medium, low | attach, import, reproduce, reject |  |

Output placeholder: <BASELINE_SHORTLIST>

## Next Route Recommendation

- Recommended route: <NEXT_ROUTE_DECISION>
- Why this route is now justified:
- Blocker if no route is responsible: <SCOUT_BLOCKER_RECORD>
- Continuity update: <SCOUT_CONTINUITY_UPDATE>
```

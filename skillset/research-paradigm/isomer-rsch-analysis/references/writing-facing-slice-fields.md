# Writing-Facing Slice Fields

Use this reference when an analysis campaign supports a paper-like deliverable
and each slice must bind to report, paper, review, or rebuttal structures. This
is the fuller writing-ready form, not the minimum required shape for every
non-paper or analysis-lite slice.

Provenance: see `provenance.md`.

## Strong Writing-Facing Slice Item

```json
{
  "exp_id": "EXP-ABL-001",
  "todo_id": "todo-ablation-core",
  "slice_id": "ablation-core",
  "title": "Core component ablation",
  "research_question": "RQ2",
  "experimental_design": "Component ablation",
  "tier": "main_required",
  "paper_placement": "main_text",
  "paper_role": "main_text",
  "section_id": "analysis-mechanism",
  "item_id": "AN-ABL-001",
  "claim_links": ["C2"],
  "analysis_role": "component ablation",
  "reviewer_question": "Is the gain caused by the proposed component or by incidental extra computation?",
  "target_display": "Main-text ablation table",
  "main_or_appendix": "main_text",
  "failure_interpretation": "If the gain remains unchanged, weaken the mechanism claim and treat the component as non-essential.",
  "completion_condition": "Show whether the central gain survives removal of the core component.",
  "why_now": "The draft cannot support the mechanism claim without this slice.",
  "success_criteria": "Produce a fair ablation under the accepted metric contract.",
  "abandonment_criteria": "Stop only if the evaluation contract becomes invalid.",
  "manuscript_targets": ["Results", "Mechanism analysis"]
}
```

## Weak Writing-Facing Slice Item

```json
{
  "slice_id": "ablation-core",
  "title": "Try one ablation",
  "research_question": "RQ2"
}
```

Why it is weak:

- no writing role
- no section id
- no item id
- no claim links
- no analysis role
- no reviewer-facing question
- no target display or failure interpretation
- no paper placement
- impossible to write back into the outline cleanly later

## Field Mapping Notes

- Use `paper_role`, `paper_placement`, `main_or_appendix`, or `tier` only when
  the report or paper contract has equivalent fields.
- If the host uses different field names, keep the semantic information and map
  the concrete schema through `[[tbd-surface:schema-evidence-item]]`.
- If the report layout is unsettled, use `[[tbd-surface:path-paper-layout]]`.

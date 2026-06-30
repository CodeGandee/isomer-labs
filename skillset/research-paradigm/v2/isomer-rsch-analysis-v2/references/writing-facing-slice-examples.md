# Writing-Facing Slice Examples

Use this reference when an analysis campaign supports a paper-like deliverable and each slice must bind to the paper, review, or rebuttal contract. This is the fuller paper-ready form, not the minimum required shape for every non-paper or analysis-lite slice. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Recover the write-back target**. Identify selected outline, paper matrix, evidence ledger, section, claim, table, reviewer item, rebuttal item, or display target before calling a slice paper-ready.
2. **Create <ANALYSIS_WRITEBACK_MAP>**. Include stable ids such as experiment id, todo id, slice id, research question, experimental design, paper role, section id, item id, claim links, analysis role, reviewer question, target display, and main or appendix role when those fields exist.
3. **State failure interpretation**. Record how a null, contradictory, or failed slice should change the paper, review answer, or route.
4. **Separate manuscript takeaway from protocol detail**. Keep internal setup, local execution notes, command history, and provenance out of manuscript-facing prose.
5. **Update the write-back target after completion**. Do not leave a completed writing-facing slice visible only as a free-floating analysis result.

## Preferences

- Prefer stable ids over free-form notes for paper-ready slices (if ids are unavailable, otherwise record the blocker or recover them).
- Prefer claim-carrying slices before supporting slices in writing-facing campaigns (if the selected narrative is already supported, otherwise deepen interpretation).
- Prefer `main_text` or `main_required` only when the slice blocks the main section (if useful but non-blocking, otherwise use `appendix` or `reference_only`).
- Prefer marking legacy-method evidence as comparator, negative, or reference-only when it is not current-method support (if intentionally included, otherwise keep it separate).

## Constraints

- Paper-ready slices must map to write-back targets, not only to local execution notes.
- Paper-facing metadata must separate manuscript takeaway from reproducibility detail and internal-only notes.
- Analysis counts must not be padded with stale methods, abandoned methods, unrelated comparator repairs, or old exploratory rows.
- A completed paper-relevant slice must not leave the paper contract stale unless the stale target is recorded as a blocker.

## Quality Gates

- Target gate: selected outline, matrix, evidence ledger, section, claim, reviewer item, rebuttal item, or display target is identified.
- Metadata gate: <ANALYSIS_WRITEBACK_MAP> includes stable ids and role fields needed for write-back.
- Failure gate: failure interpretation states how null or contradictory evidence changes the paper or route.
- Takeaway gate: manuscript-facing takeaway is separated from setup, command history, and provenance.
- Update gate: paper or review contract is updated, verified current, or marked blocked.

## Example

### Strong Writing-Facing Slice Metadata

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
  "failure_interpretation": "If the gain remains unchanged, the paper should weaken the mechanism claim and treat the component as non-essential.",
  "completion_condition": "Show whether the central gain survives removal of the core component.",
  "why_now": "The draft cannot support the mechanism claim without this slice.",
  "success_criteria": "Produce a fair ablation under the accepted metric contract.",
  "abandonment_criteria": "Stop only if the evaluation contract becomes invalid.",
  "manuscript_targets": ["Results", "Mechanism analysis"]
}
```

### Weak Writing-Facing Slice Metadata

```json
{
  "slice_id": "ablation-core",
  "title": "Try one ablation",
  "research_question": "RQ2"
}
```

This is weak because it lacks paper role, section id, item id, claim links, analysis role, reviewer-facing question, target display, paper placement, and failure interpretation.

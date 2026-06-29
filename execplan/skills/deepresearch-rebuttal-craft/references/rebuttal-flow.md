# Rebuttal flow

Writer-owned (`rebuttal` stage). Flow: **review-matrix → action-plan → evidence-update → response-letter**.
Record artifacts as `artifact.record` (kind report) under `runs/<quest-id>/report/rebuttal/`; new evidence
runs go through the Orchestrator as a `decision` route. Every supplementary run must answer a named
reviewer item id — never launch a free-floating ablation batch.

## 1. Normalize the review package → review-matrix
Atomic reviewer items with stable ids (`R1-C1`, `R1-C2`, `R2-C1`); preserve reviewer wording faithfully
(controlled head/tail ellipsis allowed; do not rewrite meaning); mark explicit vs inferred; ≥1 evidence
anchor (manuscript loc / result-table-figure / lit note / `missing_evidence`).
- Comment classes: `editorial` · `text_only` · `evidence_gap` · `experiment_gap` · `claim_scope` · `cannot_fully_address`
- Stance: `agree` · `partially_agree` · `clarify` · `respectful_disagree`
- Primary route: `text_revision` · `evidence_repackaging` · `literature_positioning` · `baseline_recovery` · `supplementary_experiment` · `claim_downgrade` · `explicit_limitation`

## 2. action-plan (the thinking draft)
Per item: id, concern-type, stance, route, why-sufficient, existing vs missing evidence. For experimental
items don't stop at "run experiment" — write hypothesis / minimal success criterion / required metrics /
**MVP plan + Enhanced plan + fallback wording**.

## 3. Route experiments only when genuinely needed
Scout first for novelty/positioning complaints; baseline first for a missing comparator; then a
`decision` → analysis-campaign, each slice tied to ≥1 reviewer id.

## 4. response-letter — drafting voice rules (the craft core)
- Rebuttal-ready AUTHOR prose, not coaching notes. Calm, direct, precise.
- Answer the concern directly in the first 1–2 sentences. Selectively concede / clarify / defend — do not
  default to conceding fault; avoid sycophancy/flattery/approval-seeking.
- Write strongly enough that a neutral AC can judge the concern substantially addressed from the rebuttal
  text alone. 1–2 full paragraphs of polished prose per item; no bullets/numbered lists/bold labels inside
  the response paragraphs.
- Use `[[AUTHOR TO FILL]]` placeholders rather than inventing specifics. Never invent results, response
  claims, or "we will add" promises; never silently ignore a hard concern; never answer with rhetoric when
  the issue requires evidence; never pretend a limitation is solved when it is only reframed.

Templates: `review-matrix-template.md`, `action-plan-template.md`, `evidence-update-template.md`,
`response-letter-template.md`.

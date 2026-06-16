# Outline contract — paper_view vs evidence_view

Ported from DeepScientist `paper-outline`. The outline is ONE selected artifact with two views. The paper
must be faithful to the evidence but must NOT echo the agent workflow. Record it as
`artifact.record` (kind `report`) under `runs/<quest-id>/report/outline.*`; the Writer gates on
`$HARNESS outline validate` before drafting.

## paper_view — what the paper says to readers
- `paper_type`, `outline_maturity`, `working_title`
- `narrative_strategy{central_thesis, central_insight, reader_takeaway}`
- `insight_ladder[]` — each rung: observed-fact → interpretation, with `evidence`, `claim_links`, `risk`
- `story_spine{problem, gap, method, main_result, scope_limit}`
- `positioning{closest_neighbor, novelty_boundary, not_claiming[]}`
- `core_claims[]` — **1–3**, each with `scope`, `evidence_needed`, **`what_would_falsify_it`**
- `method_abstraction{intuition, mechanism_steps, appendix_only_details}`
- `evaluation_plan{datasets, baselines, metrics, controlled_factors}`
- `analysis_plan[]` — **4–8 jobs** for a mature empirical paper, each with `analysis_role`,
  `reviewer_question`, `claim_links`, `target_display`, `main_or_appendix`, `failure_interpretation`
  (useful roles: component ablation, robustness/sensitivity, stronger-baseline, subgroup, failure taxonomy,
  mechanism/attribution, cost/efficiency, residual headroom)
- `reviewer_objections[]` — **≥3**, each with `answer_route ∈ {analysis, writing, claim_downgrade, limitation}`
- `evidence_grounding{observed_facts, allowed_interpretations, must_not_claim, evidence_gaps}`

## evidence_view — where the runs/rows/paths live
- `claim_to_items` (claim → supporting result/analysis/measurement/reference rows)
- `sections`, `unmapped_items`, `appendix_reproducibility`

## Hygiene
Keep engineering detail (ports, worktrees, `64+64` batch arithmetic, route decisions, "the user requested")
OUT of paper_view — it belongs in evidence_view/appendix. `outline validate` checks: a single paper idea,
scoped claims, a method abstraction, an evaluation+analysis plan, and explicit evidence boundaries.

## Quantity bars
4–8 *planned* analysis jobs to start; **5–10 ready paper-facing groups** before the paper is "strong"
(see `research-method` campaign-design + `paper-craft` section_rewrite_checklist).
